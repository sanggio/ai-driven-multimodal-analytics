from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import TextAnalysisRequest, TextAnalysisResponse
from app.core.text_analyzer import TextAnalyzer
from app.dependencies import get_text_analyzer

router = APIRouter(prefix="/api/v1/text", tags=["text"])


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    analyzer: TextAnalyzer = Depends(get_text_analyzer)
):
    try:
        result = await analyzer.analyze(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            use_cache=request.use_cache
        )
        return TextAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

