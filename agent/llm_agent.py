import asyncio
import json
import os
import sys
import time

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from groq import Groq

from security.policy import requires_confirmation
from security.confirmation import ask_confirmation
from evaluation.logger import log_result


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
        #    to Groq format
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
                    "Choose the most appropriate tool. "
                    "For email arguments, always provide the raw email "
                    "address without Markdown or mailto formatting."
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
            # model="openai/gpt-oss-120b",
            model="llama-3.3-70b-versatile",
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
        # 7. Determine operation type
        # -----------------------------

        confirmation_required = requires_confirmation(
            tool_name
        )

        tool_type = (
            "WRITE"
            if confirmation_required
            else "READ"
        )

        confirmation_given = None

        # -----------------------------
        # 8. Confirmation for writes
        # -----------------------------

        if confirmation_required:

            confirmation_given = ask_confirmation(
                tool_name,
                arguments
            )

            if not confirmation_given:

                log_result(
                    user_request=user_request,
                    expected_tool=None,
                    selected_tool=tool_name,
                    tool_type=tool_type,
                    confirmation_required=True,
                    confirmation_given=False,
                    execution_success=False,
                    execution_time_ms=0
                )

                print("\n❌ Operation blocked by user.")

                return

        # -----------------------------
        # 9. Execute MCP tool
        # -----------------------------

        print("\nExecuting tool...")

        start_time = time.perf_counter()

        try:

            result = await mcp_client.call_tool(
                tool_name,
                arguments
            )

            execution_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            execution_success = not result.is_error

            print("\nTool result:")
            print(result)

        except Exception as e:

            execution_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            execution_success = False

            print("\n❌ Tool execution failed:")
            print(e)

            result = None

        # -----------------------------
        # 10. Log evaluation data
        # -----------------------------

        log_result(
            user_request=user_request,
            expected_tool=None,
            selected_tool=tool_name,
            tool_type=tool_type,
            confirmation_required=confirmation_required,
            confirmation_given=confirmation_given,
            execution_success=execution_success,
            execution_time_ms=execution_time_ms
        )


if __name__ == "__main__":
    asyncio.run(main())