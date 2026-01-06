from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.dependencies import lifespan, get_cache_manager
from app.models.schemas import HealthResponse, MultimodalPipelineRequest, MultimodalPipelineResponse
from app.routes import text, audio, vision
from app.core.pipeline import MultimodalPipeline
from app.dependencies import get_multimodal_pipeline

app = FastAPI(
    title="AI-Driven Multimodal Analytics Gateway",
    description="High-performance Multimodal AI Gateway with FastAPI, OpenAI, and MCP Server",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router)
app.include_router(audio.router)
app.include_router(vision.router)


@app.get("/health", response_model=HealthResponse)
async def health_check(cache = Depends(get_cache_manager)):
    redis_connected = cache.redis_client is not None
    openai_configured = bool(settings.openai_api_key)
    
    return HealthResponse(
        status="healthy",
        redis_connected=redis_connected,
        openai_configured=openai_configured
    )


@app.post("/api/v1/pipeline/multimodal", response_model=MultimodalPipelineResponse)
async def multimodal_pipeline(
    request: MultimodalPipelineRequest,
    pipeline: MultimodalPipeline = Depends(get_multimodal_pipeline)
):
    tasks = []
    for task in request.tasks:
        task_dict = task.model_dump(exclude_none=True)
        tasks.append(task_dict)
    
    result = await pipeline.process_multimodal(tasks)
    return MultimodalPipelineResponse(**result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False
    )

