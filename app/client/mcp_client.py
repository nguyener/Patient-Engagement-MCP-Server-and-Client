import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPToolClient:
    def __init__(self):
        self.servers = {
            "patient": StdioServerParameters(
                command=sys.executable,
                args=["-m", "app.servers.mcp_patient_data_server"]
            ),
            "scheduling": StdioServerParameters(
                command=sys.executable,
                args=["-m", "app.servers.mcp_scheduling_server"]
            )
        }

    async def call_tool(self, server_name, tool_name, arguments):
        params = self.servers[server_name]

        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text

    async def read_resource(self, server_name, uri):
        params = self.servers[server_name]

        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.read_resource(uri)
                return "\n".join(
                    content.text
                    for content in result.contents
                    if hasattr(content, "text")
                )

    async def list_resources(self, server_name):
        params = self.servers[server_name]

        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_resources()
                return [
                    {
                        "uri": str(resource.uri),
                        "name": resource.name,
                        "description": resource.description,
                    }
                    for resource in result.resources
                ]
