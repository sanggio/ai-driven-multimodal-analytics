from contextlib import asynccontextmanager

from app.cache.redis_cache import cache_manager
from app.core.text_analyzer import TextAnalyzer
from app.core.audio_processor import AudioProcessor
from app.core.vision_analyzer import VisionAnalyzer
from app.core.pipeline import MultimodalPipeline

_text_analyzer = None
_audio_processor = None
_vision_analyzer = None
_multimodal_pipeline = None


@asynccontextmanager
async def lifespan(app):
    global _text_analyzer, _audio_processor, _vision_analyzer, _multimodal_pipeline
    
    await cache_manager.connect()
    
    _text_analyzer = TextAnalyzer()
    _audio_processor = AudioProcessor()
    _vision_analyzer = VisionAnalyzer()
    _multimodal_pipeline = MultimodalPipeline()
    
    yield
    
    await cache_manager.disconnect()


async def get_cache_manager():
    return cache_manager


async def get_text_analyzer():
    return _text_analyzer


async def get_audio_processor():
    return _audio_processor


async def get_vision_analyzer():
    return _vision_analyzer


async def get_multimodal_pipeline():
    return _multimodal_pipeline

