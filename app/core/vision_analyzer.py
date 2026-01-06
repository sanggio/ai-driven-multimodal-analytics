from typing import Optional, Any, List
import base64
import hashlib
import json

from openai import AsyncOpenAI

from app.config import settings
from app.cache.redis_cache import cache_manager


class VisionAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_vision_model

    def _encode_image(self, image_data: bytes) -> str:
        return base64.b64encode(image_data).decode('utf-8')

    def _generate_cache_key(self, images_hash: str, prompt: str) -> str:
        data = f"{images_hash}:{prompt}:{self.model}"
        return cache_manager._generate_key(data, prefix="vision")

    async def analyze(
        self,
        images: List[bytes],
        prompt: str,
        max_tokens: Optional[int] = None,
        use_cache: bool = True
    ) -> dict[str, Any]:
        images_hash = hashlib.sha256(b"".join(images)).hexdigest()
        cache_key = self._generate_cache_key(images_hash, prompt)

        if use_cache:
            cached = await cache_manager.get(cache_key)
            if cached:
                return json.loads(cached)

        content = [{"type": "text", "text": prompt}]
        
        for image_data in images:
            encoded_image = self._encode_image(image_data)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            })

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
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

    async def analyze_single(
        self,
        image: bytes,
        prompt: str,
        max_tokens: Optional[int] = None,
        use_cache: bool = True
    ) -> dict[str, Any]:
        return await self.analyze([image], prompt, max_tokens, use_cache)

