import asyncio
from typing import Any, Dict

from app.mcp.transport import MCPTransport
from app.mcp.tools import MCPToolRegistry


class MCPServer:
    def __init__(self):
        self.transport = MCPTransport()
        self.registry = MCPToolRegistry()
        self.request_id = 0

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "0.1.0",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "multimodal-analytics-mcp",
                "version": "1.0.0"
            }
        }

    async def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tools": self.registry.list_tools()
        }

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            result = await self.registry.execute_tool(tool_name, arguments)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": str(result)
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {str(e)}"
                    }
                ],
                "isError": True
            }

    async def handle_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        method = message.get("method")
        params = message.get("params", {})
        
        if method == "initialize":
            result = await self.handle_initialize(params)
        elif method == "tools/list":
            result = await self.handle_list_tools(params)
        elif method == "tools/call":
            result = await self.handle_call_tool(params)
        else:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": result
        }

    async def run(self):
        await self.transport.start()
        
        while self.transport.running:
            try:
                message = await self.transport.read_message()
                if not message:
                    break
                
                response = await self.handle_request(message)
                await self.transport.write_message(response)
            except Exception:
                break
        
        await self.transport.stop()


async def main():
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

