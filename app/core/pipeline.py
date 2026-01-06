from typing import Dict, Any, List, Optional
import asyncio

from app.core.text_analyzer import TextAnalyzer
from app.core.audio_processor import AudioProcessor
from app.core.vision_analyzer import VisionAnalyzer


class MultimodalPipeline:
    def __init__(self):
        self._modules: Dict[str, Any] = {}

    def _get_module(self, module_name: str) -> Any:
        if module_name not in self._modules:
            if module_name == "text":
                self._modules[module_name] = TextAnalyzer()
            elif module_name == "audio":
                self._modules[module_name] = AudioProcessor()
            elif module_name == "vision":
                self._modules[module_name] = VisionAnalyzer()
            else:
                raise ValueError(f"Unknown module: {module_name}")
        return self._modules[module_name]

    async def process_multimodal(
        self,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        async def execute_task(task: Dict[str, Any]) -> Dict[str, Any]:
            try:
                task_type = task.get("type")
                module = self._get_module(task_type)

                if task_type == "text":
                    result = await module.analyze(
                        prompt=task.get("prompt"),
                        system_prompt=task.get("system_prompt"),
                        temperature=task.get("temperature"),
                        max_tokens=task.get("max_tokens"),
                        use_cache=task.get("use_cache", True)
                    )
                elif task_type == "audio":
                    action = task.get("action")
                    if action == "transcribe":
                        result = await module.transcribe(
                            audio_file=task.get("audio_file"),
                            filename=task.get("filename"),
                            language=task.get("language"),
                            use_cache=task.get("use_cache", True)
                        )
                    elif action == "synthesize":
                        audio_bytes = await module.synthesize(
                            text=task.get("text"),
                            voice=task.get("voice"),
                            use_cache=task.get("use_cache", True)
                        )
                        result = {"audio_bytes": audio_bytes}
                    else:
                        raise ValueError(f"Unknown audio action: {action}")
                elif task_type == "vision":
                    result = await module.analyze(
                        images=task.get("images"),
                        prompt=task.get("prompt"),
                        max_tokens=task.get("max_tokens"),
                        use_cache=task.get("use_cache", True)
                    )
                else:
                    raise ValueError(f"Unknown task type: {task_type}")

                return {"status": "success", "type": task_type, "result": result}
            except Exception as e:
                return {"status": "error", "type": task.get("type"), "error": str(e)}

        results = await asyncio.gather(*[execute_task(task) for task in tasks], return_exceptions=True)

        return {
            "total_tasks": len(tasks),
            "successful": sum(1 for r in results if isinstance(r, dict) and r.get("status") == "success"),
            "failed": sum(1 for r in results if isinstance(r, dict) and r.get("status") == "error"),
            "results": [r if isinstance(r, dict) else {"status": "error", "error": str(r)} for r in results]
        }

