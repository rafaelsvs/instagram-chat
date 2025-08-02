# Instagram Chatbot com FastAPI

Este projeto implementa um chatbot integrado ao Instagram usando a API Graph do Meta e FastAPI como backend.

## Funcionalidades

- Recebe mensagens via Webhook do Instagram
- Processa comentários e mensagens diretas (DMs)
- Envia respostas automáticas
- Integração com banco de dados PostgreSQL
- Deploy local com ngrok para testes

## Como usar

1. **Clone o repositório**  
```bash
git clone https://github.com/rafaelsvs/instagram-chat.git
cd instagram-chat
```

2. **Configure as variáveis de ambiente no `.env`**  
```env
PAGE_ACCESS_TOKEN=seu_token
VERIFY_TOKEN=seu_token_de_verificacao
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_db
```

3. **Inicie o servidor FastAPI**  
```bash
uvicorn main:app --reload
```

4. **Exponha com ngrok (para testes)**  
```bash
ngrok http 8000
```

5. **Configure o Webhook no Meta Developer**

- URL de callback: `https://<ngrok>/webhook`
- Token de verificação: o mesmo do `.env`
- Permissões: `pages_manage_metadata`, `instagram_manage_messages`, `instagram_basic`, etc.

## Endpoints

- `GET /webhook`: validação do webhook
- `POST /webhook`: recebe mensagens do Instagram
- `POST /webhook/test`: teste manual com payload simulado

## Estrutura

```
.
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── db/
│   └── services/
├── .env
├── main.py
└── requirements.txt
```

## Licença

MIT
