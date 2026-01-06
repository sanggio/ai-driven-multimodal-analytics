from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response

from app.models.schemas import (
    AudioTranscriptionRequest,
    AudioTranscriptionResponse,
    AudioSynthesisRequest
)
from app.core.audio_processor import AudioProcessor
from app.dependencies import get_audio_processor

router = APIRouter(prefix="/api/v1/audio", tags=["audio"])


@router.post("/transcribe", response_model=AudioTranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = None,
    use_cache: bool = True,
    processor: AudioProcessor = Depends(get_audio_processor)
):
    try:
        audio_bytes = await file.read()
        result = await processor.transcribe(
            audio_file=audio_bytes,
            filename=file.filename,
            language=language,
            use_cache=use_cache
        )
        return AudioTranscriptionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synthesize")
async def synthesize_speech(
    request: AudioSynthesisRequest,
    processor: AudioProcessor = Depends(get_audio_processor)
):
    try:
        audio_bytes = await processor.synthesize(
            text=request.text,
            voice=request.voice,
            use_cache=request.use_cache
        )
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

