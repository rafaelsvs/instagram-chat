from fastapi import FastAPI
from app.api.routes import webhook
from app.db.database import engine, Base

app = FastAPI()

# Criação das tabelas no banco (idealmente via migrations em produção)
Base.metadata.create_all(bind=engine)

# Rotas
app.include_router(webhook.router, prefix="/webhook", tags=["Instagram Webhook"])
