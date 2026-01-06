from typing import Any, Dict, List, Optional
import base64

from app.core.text_analyzer import TextAnalyzer
from app.core.audio_processor import AudioProcessor
from app.core.vision_analyzer import VisionAnalyzer


class MCPToolRegistry:
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.audio_processor = AudioProcessor()
        self.vision_analyzer = VisionAnalyzer()
        self.tools = {
            "analyze_text": self._analyze_text,
            "transcribe_audio": self._transcribe_audio,
            "synthesize_speech": self._synthesize_speech,
            "analyze_image": self._analyze_image,
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "analyze_text",
                "description": "Analyze text using LLM",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string"},
                        "system_prompt": {"type": "string"},
                        "temperature": {"type": "number"},
                        "max_tokens": {"type": "integer"}
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "transcribe_audio",
                "description": "Transcribe audio to text using Whisper",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "audio_base64": {"type": "string"},
                        "filename": {"type": "string"},
                        "language": {"type": "string"}
                    },
                    "required": ["audio_base64", "filename"]
                }
            },
            {
                "name": "synthesize_speech",
                "description": "Synthesize speech from text using TTS",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "voice": {"type": "string"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "analyze_image",
                "description": "Analyze images using Vision API",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "images_base64": {"type": "array", "items": {"type": "string"}},
                        "prompt": {"type": "string"},
                        "max_tokens": {"type": "integer"}
                    },
                    "required": ["images_base64", "prompt"]
                }
            }
        ]

    async def _analyze_text(self, **kwargs) -> Dict[str, Any]:
        return await self.text_analyzer.analyze(
            prompt=kwargs.get("prompt"),
            system_prompt=kwargs.get("system_prompt"),
            temperature=kwargs.get("temperature"),
            max_tokens=kwargs.get("max_tokens")
        )

    async def _transcribe_audio(self, **kwargs) -> Dict[str, Any]:
        audio_base64 = kwargs.get("audio_base64")
        audio_bytes = base64.b64decode(audio_base64)
        return await self.audio_processor.transcribe(
            audio_file=audio_bytes,
            filename=kwargs.get("filename"),
            language=kwargs.get("language")
        )

    async def _synthesize_speech(self, **kwargs) -> Dict[str, Any]:
        audio_bytes = await self.audio_processor.synthesize(
            text=kwargs.get("text"),
            voice=kwargs.get("voice")
        )
        return {
            "audio_base64": base64.b64encode(audio_bytes).decode('utf-8')
        }

    async def _analyze_image(self, **kwargs) -> Dict[str, Any]:
        images_base64 = kwargs.get("images_base64", [])
        images = [base64.b64decode(img) for img in images_base64]
        return await self.vision_analyzer.analyze(
            images=images,
            prompt=kwargs.get("prompt"),
            max_tokens=kwargs.get("max_tokens")
        )

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool_func = self.tools[tool_name]
        return await tool_func(**arguments)

