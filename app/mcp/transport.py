import sys
import json
import asyncio
from typing import Any, Dict

from app.mcp.tools import MCPToolRegistry


class MCPTransport:
    def __init__(self):
        self.running = False

    async def read_message(self) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            return {}
        return json.loads(line.strip())

    async def write_message(self, message: Dict[str, Any]):
        output = json.dumps(message) + "\n"
        sys.stdout.write(output)
        sys.stdout.flush()

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False

