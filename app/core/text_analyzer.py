from typing import Optional, Any
import base64
import hashlib
import json

from openai import AsyncOpenAI

from app.config import settings
from app.cache.redis_cache import cache_manager


class TextAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def _generate_cache_key(self, prompt: str, model: str) -> str:
        data = f"{prompt}:{model}"
        return cache_manager._generate_key(data, prefix="text")

    async def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_cache: bool = True
    ) -> dict[str, Any]:
        cache_key = self._generate_cache_key(prompt, self.model)

        if use_cache:
            cached = await cache_manager.get(cache_key)
            if cached:
                return json.loads(cached)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or settings.temperature,
            max_tokens=max_tokens or settings.max_tokens
        )

        result = {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }

        if use_cache:
            await cache_manager.set(cache_key, result)

        return result

