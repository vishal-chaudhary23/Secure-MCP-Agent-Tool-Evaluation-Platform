import asyncio
import json
import os

import sys
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from groq import Groq


load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



transport = StdioTransport(
    command=sys.executable,
    args=["-m", "mcp_servers.user_server"]
)

mcp_client = Client(transport)


async def main():

    async with mcp_client:

        # -----------------------------
        # 1. Discover MCP tools
        # -----------------------------

        tools = await mcp_client.list_tools()

        print("Available MCP tools:")

        for tool in tools:
            print(f"- {tool.name}")

        # -----------------------------
        # 2. Convert MCP tools
        #    to Groq/OpenAI format
        # -----------------------------

        groq_tools = []

        for tool in tools:

            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })

        # -----------------------------
        # 3. Get user request
        # -----------------------------

        user_request = input("\nYou: ")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an enterprise assistant. "
                    "Use the available tools to fulfill the user's request. "
                    "Choose the most appropriate tool."
                )
            },
            {
                "role": "user",
                "content": user_request
            }
        ]

        # -----------------------------
        # 4. Ask Groq to select tool
        # -----------------------------

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=groq_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # -----------------------------
        # 5. No tool selected
        # -----------------------------

        if not message.tool_calls:

            print("\nAgent:")
            print(message.content)

            return

        # -----------------------------
        # 6. Get selected tool
        # -----------------------------

        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("\nSelected tool:")
        print(tool_name)

        print("\nArguments:")
        print(arguments)

        # -----------------------------
        # 7. Execute MCP tool
        # -----------------------------

        result = await mcp_client.call_tool(
            tool_name,
            arguments
        )

        print("\nTool result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())