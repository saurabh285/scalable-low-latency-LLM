from fastapi import FastAPI
from app.router import router

app = FastAPI(
    title="Scalable QnA Assistant",
    description="Fast, LLM-Augmented, Low-Latency QnA API",
    version="1.0.0"
)

app.include_router(router)
