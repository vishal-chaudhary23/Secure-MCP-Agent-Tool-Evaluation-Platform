import asyncio
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


transport = StdioTransport(
    command=sys.executable,
    args=["-m", "mcp_servers.user_server"]
)

client = Client(transport)


async def main():

    async with client:

        print("Connected to MCP server!")

        tools = await client.list_tools()

        print("\nAvailable tools:")

        for tool in tools:
            print(f"- {tool.name}")
            print(f"  Description: {tool.description}")

        # Read operation
        result = await client.call_tool(
            "get_user",
            {
                "user_id": 1
            }
        )

        print("\nGet user result:")
        print(result)


        # Modification operation
        result = await client.call_tool(
            "update_user_email",
            {
                "user_id": 1,
                "email": "vishal_new@example.com"
            }
        )

        print("\nUpdate result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())