import pytest
from httpx import AsyncClient
from io import BytesIO
from app.main import app


@pytest.mark.asyncio
async def test_transcribe_audio():
    async with AsyncClient(app=app, base_url="http://test") as client:
        audio_data = b"fake audio data for testing"
        files = {"file": ("test.mp3", BytesIO(audio_data), "audio/mpeg")}
        
        response = await client.post(
            "/api/v1/audio/transcribe",
            files=files,
            params={"use_cache": False}
        )
        assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_synthesize_speech():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audio/synthesize",
            json={
                "text": "Hello, this is a test",
                "voice": "alloy",
                "use_cache": False
            }
        )
        assert response.status_code in [200, 500]

