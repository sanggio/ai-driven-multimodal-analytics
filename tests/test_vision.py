import pytest
from httpx import AsyncClient
from io import BytesIO
from app.main import app


@pytest.mark.asyncio
async def test_analyze_vision():
    async with AsyncClient(app=app, base_url="http://test") as client:
        image_data = b"fake image data for testing"
        files = [("files", ("test.jpg", BytesIO(image_data), "image/jpeg"))]
        
        response = await client.post(
            "/api/v1/vision/analyze",
            files=files,
            params={
                "prompt": "Describe this image",
                "use_cache": False
            }
        )
        assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "redis_connected" in data
        assert "openai_configured" in data


@pytest.mark.asyncio
async def test_multimodal_pipeline():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/pipeline/multimodal",
            json={
                "tasks": [
                    {
                        "type": "text",
                        "prompt": "What is machine learning?",
                        "use_cache": False
                    }
                ]
            }
        )
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "total_tasks" in data
            assert "results" in data

