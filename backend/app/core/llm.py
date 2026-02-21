"""
OpenAI / Azure OpenAI integration.

Supports both Azure OpenAI (default for enterprise) and OpenAI directly.
Set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT for Azure,
or OPENAI_API_KEY for OpenAI.

Usage:
    from app.core.llm import llm_complete, llm_stream

    response = await llm_complete("What is 2+2?")

    async for chunk in llm_stream("Tell me a story"):
        print(chunk)
"""

from collections.abc import AsyncGenerator

from openai import AsyncAzureOpenAI, AsyncOpenAI

from app.core.config import get_settings


def _get_client() -> AsyncOpenAI:
    """Build the appropriate OpenAI client based on config."""
    settings = get_settings()

    if settings.azure_openai_api_key and settings.azure_openai_endpoint:
        return AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )

    if settings.openai_api_key:
        return AsyncOpenAI(api_key=settings.openai_api_key)

    raise RuntimeError(
        "No LLM provider configured. "
        "Set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT, "
        "or OPENAI_API_KEY in your .env file."
    )


async def llm_complete(
    prompt: str,
    model: str | None = None,
    system_prompt: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str:
    """Get a completion from the configured LLM."""
    settings = get_settings()
    client = _get_client()
    model = model or settings.llm_model

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


async def llm_stream(
    prompt: str,
    model: str | None = None,
    system_prompt: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> AsyncGenerator[str, None]:
    """Stream a completion from the configured LLM. Works with WebSockets and SSE."""
    settings = get_settings()
    client = _get_client()
    model = model or settings.llm_model

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    async for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
