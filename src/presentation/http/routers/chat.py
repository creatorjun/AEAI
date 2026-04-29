# src/presentation/http/routers/chat.py
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from src.presentation.http.schemas.chat import ChatRequest, ChatResponse, UsageSchema, ToolCallSchema
from src.presentation.http.dependencies.usecases import get_create_chat, get_stream_chat
from src.application.usecases.create_chat_completion import CreateChatCompletion
from src.application.usecases.stream_chat_completion import StreamChatCompletion
from src.domain.errors.domain_errors import ConversationNotFoundError, InferenceError
from src.infrastructure.config.settings import get_settings
import json

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completions", response_model=ChatResponse)
async def create_completion(
    body: ChatRequest,
    usecase: CreateChatCompletion = Depends(get_create_chat),
) -> ChatResponse:
    settings = get_settings()
    model = body.model or settings.default_model
    try:
        response, conv_id = await usecase.execute(
            conversation_id=body.conversation_id,
            user_message=body.message,
            model=model,
            temperature=body.temperature,
            max_tokens=body.max_tokens,
            system_prompt=body.system_prompt,
        )
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InferenceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
    return ChatResponse(
        conversation_id=conv_id,
        content=response.content,
        model=response.model,
        usage=UsageSchema(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        ),
        tool_calls=[
            ToolCallSchema(id=tc.id, tool_name=tc.tool_name, arguments=tc.arguments)
            for tc in response.tool_calls
        ],
        finish_reason=response.finish_reason,
        cached=response.cached,
    )


@router.post("/stream")
async def stream_completion(
    body: ChatRequest,
    usecase: StreamChatCompletion = Depends(get_stream_chat),
) -> StreamingResponse:
    settings = get_settings()
    model = body.model or settings.default_model
    try:
        gen = await usecase.execute(
            conversation_id=body.conversation_id,
            user_message=body.message,
            model=model,
            temperature=body.temperature,
            max_tokens=body.max_tokens,
            system_prompt=body.system_prompt,
        )
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def event_stream():
        async for chunk in gen:
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
