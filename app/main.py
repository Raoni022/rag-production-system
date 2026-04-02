from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="RAG Production System")
app.include_router(router)
