from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
from app.services.flow_manager import process_message
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()  # Carrega as variáveis do .env

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Agora busca do .env

@router.get("")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)
    return PlainTextResponse("Invalid verification", status_code=403)

@router.post("")
async def receive_event(req: Request):
    body = await req.json()
    print("📦 Recebido:", body)
    await process_message(body)
    return {"status": "received"}

@router.post("/{path:path}")
async def catch_all_events(req: Request, path: str):
    body = await req.json()
    print(f"📥 Evento recebido em /webhook/{path}:", body)

    # Você pode adicionar lógica condicional se quiser tratar por tipo
    await process_message(body)
    return {"status": "received"}


@router.post("/test")
async def receive_meta_test_event(req: Request):
    body = await req.json()
    print("🔥 Chegou do Meta (teste):", body)

    value = body.get("value", {})
    sender_id = value.get("sender", {}).get("id")
    text = value.get("message", {}).get("text", "")

    if sender_id and "ebook" in text.lower():
        from app.core.meta_api import send_message
        send_message(sender_id, "Legal! Me envia seu *email* pra continuar.")

    return {"status": "received"}