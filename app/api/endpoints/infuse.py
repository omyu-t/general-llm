from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services import openai_service

router = APIRouter()

@router.get("/openai-stream/")
async def read_openai(question: str):
    return StreamingResponse(
        openai_service.chat_openai_stream(question), media_type="text/event-stream"
    )


@router.get("/openai/")
async def read_openai_final(question: str):
    return await openai_service.chat_openai(question)