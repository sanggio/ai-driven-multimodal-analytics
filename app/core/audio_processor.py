from typing import Optional, Any
import hashlib
import json

from openai import AsyncOpenAI

from app.config import settings
from app.cache.redis_cache import cache_manager


class AudioProcessor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.whisper_model = settings.openai_audio_model
        self.tts_model = settings.openai_tts_model
        self.tts_voice = settings.openai_tts_voice

    def _generate_cache_key(self, data: bytes, prefix: str) -> str:
        hash_obj = hashlib.sha256(data)
        return f"{prefix}:{hash_obj.hexdigest()}"

    async def transcribe(
        self,
        audio_file: bytes,
        filename: str,
        language: Optional[str] = None,
        use_cache: bool = True
    ) -> dict[str, Any]:
        cache_key = self._generate_cache_key(audio_file, prefix="transcribe")

        if use_cache:
            cached = await cache_manager.get(cache_key)
            if cached:
                return json.loads(cached)

        response = await self.client.audio.transcriptions.create(
            model=self.whisper_model,
            file=(filename, audio_file),
            language=language
        )

        result = {
            "text": response.text,
            "model": self.whisper_model
        }

        if use_cache:
            await cache_manager.set(cache_key, result)

        return result

    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        use_cache: bool = True
    ) -> bytes:
        cache_key = cache_manager._generate_key(f"{text}:{voice or self.tts_voice}", prefix="tts")

        if use_cache:
            cached = await cache_manager.get(cache_key)
            if cached:
                return json.loads(cached).encode('latin1')

        response = await self.client.audio.speech.create(
            model=self.tts_model,
            voice=voice or self.tts_voice,
            input=text
        )

        audio_bytes = response.content

        if use_cache:
            await cache_manager.set(cache_key, audio_bytes.decode('latin1'))

        return audio_bytes

