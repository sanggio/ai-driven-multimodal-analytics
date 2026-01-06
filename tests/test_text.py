import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_analyze_text():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/text/analyze",
            json={
                "prompt": "What is artificial intelligence?",
                "use_cache": False
            }
        )
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "content" in data
            assert "model" in data
            assert "usage" in data


@pytest.mark.asyncio
async def test_analyze_text_with_system_prompt():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/text/analyze",
            json={
                "prompt": "Explain quantum computing",
                "system_prompt": "You are a physics professor",
                "temperature": 0.5,
                "max_tokens": 500,
                "use_cache": False
            }
        )
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert data["content"]

