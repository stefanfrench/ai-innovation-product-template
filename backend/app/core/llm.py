"""
LiteLLM integration for unified LLM access.
Supports OpenAI, Azure OpenAI, Anthropic, Ollama (local), and 100+ providers.

Usage:
    from app.core.llm import llm_complete, llm_stream

    # Simple completion
    response = await llm_complete("What is 2+2?")

    # Streaming (for WebSocket/SSE)
    async for chunk in llm_stream("Tell me a story"):
        print(chunk)

    # Override model per-request
    response = await llm_complete("Hello", model="claude-3-sonnet-20240229")
"""

from collections.abc import AsyncGenerator
from typing import Any

import litellm
from litellm import acompletion

from app.core.config import get_settings

settings = get_settings()

# Configure LiteLLM
litellm.set_verbose = settings.debug


def _get_completion_kwargs(model: str | None = None) -> dict[str, Any]:
    """Build kwargs for LiteLLM based on settings."""
    model = model or settings.litellm_model
    kwargs: dict[str, Any] = {"model": model}

    # Azure OpenAI
    if model.startswith("azure/") and settings.azure_api_key:
        kwargs["api_key"] = settings.azure_api_key
        kwargs["api_base"] = settings.azure_api_base
        kwargs["api_version"] = settings.azure_api_version

    # OpenAI
    elif settings.openai_api_key and not model.startswith(("ollama/", "claude")):
        kwargs["api_key"] = settings.openai_api_key

    # Anthropic
    elif model.startswith("claude") and settings.anthropic_api_key:
        kwargs["api_key"] = settings.anthropic_api_key

    # Ollama (local)
    elif model.startswith("ollama/"):
        kwargs["api_base"] = settings.ollama_base_url

    return kwargs


async def llm_complete(
    prompt: str,
    model: str | None = None,
    system_prompt: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str:
    """
    Get a completion from the configured LLM.

    Args:
        prompt: User message/prompt
        model: Override the default model (e.g., "gpt-4o", "azure/gpt-4", "ollama/llama2")
        system_prompt: Optional system message
        temperature: Creativity (0-2)
        max_tokens: Maximum response length

    Returns:
        The LLM's response text
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    kwargs = _get_completion_kwargs(model)

    response = await acompletion(
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )

    return response.choices[0].message.content


async def llm_stream(
    prompt: str,
    model: str | None = None,
    system_prompt: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> AsyncGenerator[str, None]:
    """
    Stream a completion from the configured LLM.
    Perfect for WebSocket streaming or Server-Sent Events.

    Args:
        prompt: User message/prompt
        model: Override the default model
        system_prompt: Optional system message
        temperature: Creativity (0-2)
        max_tokens: Maximum response length

    Yields:
        Text chunks as they arrive
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    kwargs = _get_completion_kwargs(model)

    response = await acompletion(
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        **kwargs,
    )

    async for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
