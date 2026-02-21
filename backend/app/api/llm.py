"""
LLM API endpoints.
Provides both REST and WebSocket access to LLM capabilities.
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.core.llm import llm_complete, llm_stream


def _check_llm_configured(settings) -> None:
    """Raise a clear error if no LLM provider API key is set."""
    has_key = settings.azure_openai_api_key or settings.openai_api_key
    if not has_key:
        raise HTTPException(
            status_code=503,
            detail=(
                "No LLM provider configured. "
                "Set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT for Azure OpenAI, "
                "or OPENAI_API_KEY for OpenAI in your .env file."
            ),
        )

router = APIRouter(prefix="/llm", tags=["llm"])


class CompletionRequest(BaseModel):
    """Request body for LLM completion."""

    prompt: str
    model: str | None = None
    system_prompt: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1000


class CompletionResponse(BaseModel):
    """Response from LLM completion."""

    content: str
    model: str


@router.post("/complete", response_model=CompletionResponse)
async def complete(request: CompletionRequest) -> CompletionResponse:
    """
    Get a completion from the LLM.

    Example:
    ```
    POST /api/llm/complete
    {
        "prompt": "Explain quantum computing in simple terms",
        "temperature": 0.7
    }
    ```
    """
    from app.core.config import get_settings

    settings = get_settings()
    _check_llm_configured(settings)

    content = await llm_complete(
        prompt=request.prompt,
        model=request.model,
        system_prompt=request.system_prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return CompletionResponse(
        content=content,
        model=request.model or settings.llm_model,
    )


@router.websocket("/stream")
async def stream_completion(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for streaming LLM responses.

    Connect and send JSON messages:
    ```json
    {
        "prompt": "Tell me a story about a robot",
        "system_prompt": "You are a creative storyteller",
        "temperature": 0.8
    }
    ```

    Receives streamed text chunks, then a final {"done": true} message.
    """
    await websocket.accept()

    from app.core.config import get_settings
    settings = get_settings()

    try:
        while True:
            data = await websocket.receive_json()

            prompt = data.get("prompt", "")
            if not prompt:
                await websocket.send_json({"error": "prompt is required"})
                continue

            try:
                _check_llm_configured(settings)
            except HTTPException as e:
                await websocket.send_json({"error": e.detail})
                continue

            try:
                async for chunk in llm_stream(
                    prompt=prompt,
                    model=data.get("model"),
                    system_prompt=data.get("system_prompt"),
                    temperature=data.get("temperature", 0.7),
                    max_tokens=data.get("max_tokens", 1000),
                ):
                    await websocket.send_json({"chunk": chunk})

                await websocket.send_json({"done": True})

            except Exception as e:
                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        pass
