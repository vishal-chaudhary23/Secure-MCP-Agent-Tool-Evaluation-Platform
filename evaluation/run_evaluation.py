import asyncio
import os
import sys
from collections import defaultdict

from dotenv import load_dotenv
from groq import Groq
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from evaluation.test_cases import TEST_CASES


load_dotenv()


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def run():

    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "mcp_servers.user_server"]
    )

    mcp_client = Client(transport)

    async with mcp_client:

        tools = await mcp_client.list_tools()

        groq_tools = []

        for tool in tools:

            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            })

        total = len(TEST_CASES)
        correct = 0
        wrong = 0

        # Per-tool statistics
        stats = defaultdict(
            lambda: {
                "total": 0,
                "correct": 0,
                "wrong": 0,
            }
        )

        print(
            "\n========== TOOL SELECTION EVALUATION ==========\n"
        )

        for index, test in enumerate(TEST_CASES, start=1):

            request = test["request"]
            expected = test["expected_tool"]

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an enterprise assistant. "
                            "Select the single most appropriate "
                            "tool for the user's request."
                        ),
                    },
                    {
                        "role": "user",
                        "content": request,
                    },
                ],
                tools=groq_tools,
                tool_choice="auto",
            )

            message = response.choices[0].message

            if message.tool_calls:

                selected = (
                    message.tool_calls[0]
                    .function
                    .name
                )

            else:

                selected = None

            is_correct = selected == expected

            if is_correct:
                correct += 1
            else:
                wrong += 1

            stats[expected]["total"] += 1

            if is_correct:
                stats[expected]["correct"] += 1
            else:
                stats[expected]["wrong"] += 1

            print(f"[{index}/{total}]")
            print(f"Request:  {request}")
            print(f"Expected: {expected}")
            print(f"Selected: {selected}")
            print(
                f"Result:   "
                f"{'CORRECT' if is_correct else 'WRONG'}"
            )
            print("-" * 50)

        # =====================================
        # Overall metrics
        # =====================================

        accuracy = (
            correct / total * 100
            if total
            else 0
        )

        print("\n========== OVERALL SUMMARY ==========")

        print(f"Total tests:       {total}")
        print(f"Correct tools:     {correct}")
        print(f"Wrong tools:       {wrong}")
        print(f"Accuracy:          {accuracy:.2f}%")

        # =====================================
        # Per-tool metrics
        # =====================================

        print("\n========== PER-TOOL ACCURACY ==========")

        for tool_name, data in stats.items():

            tool_accuracy = (
                data["correct"]
                / data["total"]
                * 100
            )

            print(
                f"{tool_name:<25}"
                f"{tool_accuracy:>7.2f}%   "
                f"({data['correct']}/{data['total']})"
            )


if __name__ == "__main__":
    asyncio.run(run())