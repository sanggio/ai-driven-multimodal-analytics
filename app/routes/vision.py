from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List

from app.models.schemas import VisionAnalysisRequest, VisionAnalysisResponse
from app.core.vision_analyzer import VisionAnalyzer
from app.dependencies import get_vision_analyzer

router = APIRouter(prefix="/api/v1/vision", tags=["vision"])


@router.post("/analyze", response_model=VisionAnalysisResponse)
async def analyze_images(
    files: List[UploadFile] = File(...),
    prompt: str = "Describe this image",
    max_tokens: int = None,
    use_cache: bool = True,
    analyzer: VisionAnalyzer = Depends(get_vision_analyzer)
):
    try:
        images = []
        for file in files:
            image_bytes = await file.read()
            images.append(image_bytes)
        
        result = await analyzer.analyze(
            images=images,
            prompt=prompt,
            max_tokens=max_tokens,
            use_cache=use_cache
        )
        return VisionAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

