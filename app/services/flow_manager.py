from app.db.database import SessionLocal
from app.db.models import Lead
from app.core.meta_api import send_message, get_user_info

# Vamos simular o estado da conversa em memória (usar Redis depois)
user_states = {}

async def process_message(payload):
    if "entry" not in payload:
        return

    for entry in payload["entry"]:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            field = change.get("field", "")

            # 👇 Trata comentários no Instagram (feed, reels, etc)
            if field == "comments":
                comment_text = value.get("text", "").strip().lower()
                user_id = value.get("from", {}).get("id")

                if "ebook" in comment_text:
                    send_message(user_id, "Oi! Vi seu comentário. Me envia seu *email* aqui na DM pra continuar?")
                    user_states[user_id] = "awaiting_email"
                    return

            # 👇 Trata mensagens diretas no WhatsApp
            messages = value.get("messages", [])
            for msg in messages:
                user_id = msg["from"]
                text = msg["text"]["body"].strip().lower()

                state = user_states.get(user_id, "awaiting_keyword")

                if state == "awaiting_keyword":
                    if "ebook" in text:
                        send_message(user_id, "Legal! Me envia seu *email* pra continuar.")
                        user_states[user_id] = "awaiting_email"

                elif state == "awaiting_email":
                    if "@" in text:
                        user_states[user_id] = {"email": text, "step": "awaiting_phone"}
                        send_message(user_id, "Show! Agora me envia seu telefone com DDD.")
                    else:
                        send_message(user_id, "Hmm, isso não parece um email válido...")

                elif isinstance(state, dict) and state.get("step") == "awaiting_phone":
                    phone = text
                    email = state["email"]

                    user_info = get_user_info(user_id)
                    username = user_info.get("username", "")
                    full_name = user_info.get("full_name", "")

                    db = SessionLocal()
                    db.add(Lead(
                        instagram_id=user_id,
                        username=username,
                        full_name=full_name,
                        email=email,
                        phone=phone,
                        origin="DM"
                    ))
                    db.commit()
                    db.close()

                    send_message(user_id, "Pronto, você está na minha lista. Em breve novidades!")
                    user_states[user_id] = "completed"
