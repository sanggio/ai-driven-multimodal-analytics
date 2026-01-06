from pydantic import BaseModel, Field
from typing import Optional, List, Any


class TextAnalysisRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for analysis")
    system_prompt: Optional[str] = Field(None, description="System prompt for context")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, gt=0, description="Maximum tokens in response")
    use_cache: bool = Field(True, description="Use caching for responses")


class TextAnalysisResponse(BaseModel):
    content: str
    model: str
    usage: dict


class AudioTranscriptionRequest(BaseModel):
    language: Optional[str] = Field(None, description="Language code for transcription")
    use_cache: bool = Field(True, description="Use caching for responses")


class AudioTranscriptionResponse(BaseModel):
    text: str
    model: str


class AudioSynthesisRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize")
    voice: Optional[str] = Field(None, description="Voice to use for synthesis")
    use_cache: bool = Field(True, description="Use caching for responses")


class VisionAnalysisRequest(BaseModel):
    prompt: str = Field(..., description="Analysis prompt for images")
    max_tokens: Optional[int] = Field(None, gt=0, description="Maximum tokens in response")
    use_cache: bool = Field(True, description="Use caching for responses")


class VisionAnalysisResponse(BaseModel):
    content: str
    model: str
    usage: dict


class MultimodalTask(BaseModel):
    type: str = Field(..., description="Task type: text, audio, or vision")
    action: Optional[str] = Field(None, description="Action for audio: transcribe or synthesize")
    prompt: Optional[str] = Field(None, description="Prompt for text or vision tasks")
    system_prompt: Optional[str] = Field(None, description="System prompt for text tasks")
    text: Optional[str] = Field(None, description="Text for audio synthesis")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    voice: Optional[str] = Field(None, description="Voice for TTS")
    language: Optional[str] = Field(None, description="Language for transcription")
    use_cache: bool = Field(True, description="Use caching")


class MultimodalPipelineRequest(BaseModel):
    tasks: List[MultimodalTask] = Field(..., description="List of tasks to execute")


class MultimodalPipelineResponse(BaseModel):
    total_tasks: int
    successful: int
    failed: int
    results: List[dict]


class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
    openai_configured: bool

