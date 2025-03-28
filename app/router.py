from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.cache import redis_get, redis_set
from app.vector import search_faiss, add_to_knowledge_base
from app.gemini import stream_gemini_response
import time

router = APIRouter()

@router.get("/ask")
async def ask(q: str, request: Request):
    start = time.time()

    # 1. Redis
    redis_start = time.time()
    cached = redis_get(q)
    redis_time = time.time() - redis_start

    if cached:
        total = time.time() - start
        return {
            "source": "redis",
            "answer": cached,
            "latency_ms": round(total * 1000, 2),
            "breakdown": {
                "redis_ms": round(redis_time * 1000, 2)
            }
        }

    # 2. FAISS
    faiss_start = time.time()
    faiss_answer = search_faiss(q)
    faiss_time = time.time() - faiss_start

    if faiss_answer:
        redis_set(q, faiss_answer)
        total = time.time() - start
        return {
            "source": "faiss",
            "answer": faiss_answer,
            "latency_ms": round(total * 1000, 2),
            "breakdown": {
                "redis_ms": round(redis_time * 1000, 2),
                "faiss_ms": round(faiss_time * 1000, 2)
            }
        }

    # 3. Gemini Streaming (fallback)
    async def gemini_stream():
        gemini_start = time.time()
        response = ""
        async for chunk in stream_gemini_response(q):
            response += chunk
            yield chunk
        gemini_time = time.time() - gemini_start

        redis_set(q, response)
        add_to_knowledge_base(q, response)

    return StreamingResponse(gemini_stream(), media_type="text/plain")
