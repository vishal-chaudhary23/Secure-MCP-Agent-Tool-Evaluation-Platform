import asyncio
import os
import sys
from collections import defaultdict

from dotenv import load_dotenv
from groq import Groq, BadRequestError
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from evaluation.test_cases import TEST_CASES


load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv(
    "EVAL_MODEL",
    "openai/gpt-oss-120b"
)


async def run():

    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "mcp_servers.user_server"]
    )

    mcp_client = Client(transport)

    async with mcp_client:

        # -----------------------------
        # Discover MCP tools
        # -----------------------------

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
        tool_call_failures = 0
        no_tool_selected = 0

        stats = defaultdict(
            lambda: {
                "total": 0,
                "correct": 0,
                "wrong": 0,
                "failures": 0,
            }
        )

        wrong_cases = []
        failure_cases = []

        print(
            f"\nEvaluation Model: {MODEL}"
        )

        print(
            "\n========== TOOL SELECTION EVALUATION ==========\n"
        )

        # =========================================
        # Run benchmark
        # =========================================

        for index, test in enumerate(
            TEST_CASES,
            start=1
        ):

            request = test["request"]
            expected = test["expected_tool"]

            try:

                response = groq_client.chat.completions.create(

                    model=MODEL,

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an enterprise assistant. "
                                "Select the single most appropriate "
                                "tool for the user's request. "
                                "Use valid structured tool calling."
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

            except BadRequestError as e:

                tool_call_failures += 1

                stats[expected]["total"] += 1
                stats[expected]["failures"] += 1

                failure_cases.append({
                    "request": request,
                    "expected": expected,
                    "error": str(e),
                })

                print(f"[{index}/{total}]")
                print(f"Request:  {request}")
                print(f"Expected: {expected}")
                print("Selected: None")
                print("Result:   TOOL-CALL FAILURE")
                print("-" * 50)

                continue

            message = response.choices[0].message

            # =========================================
            # No tool selected
            # =========================================

            if not message.tool_calls:

                selected = None

                no_tool_selected += 1

                stats[expected]["total"] += 1
                stats[expected]["wrong"] += 1

                wrong_cases.append({
                    "request": request,
                    "expected": expected,
                    "selected": None,
                })

                print(f"[{index}/{total}]")
                print(f"Request:  {request}")
                print(f"Expected: {expected}")
                print("Selected: None")
                print("Result:   NO TOOL SELECTED")
                print("-" * 50)

                continue

            # =========================================
            # Tool selected
            # =========================================

            selected = (
                message
                .tool_calls[0]
                .function
                .name
            )

            is_correct = (
                selected == expected
            )

            stats[expected]["total"] += 1

            if is_correct:

                correct += 1
                stats[expected]["correct"] += 1

                result_text = "CORRECT"

            else:

                wrong += 1
                stats[expected]["wrong"] += 1

                wrong_cases.append({
                    "request": request,
                    "expected": expected,
                    "selected": selected,
                })

                result_text = "WRONG"

            print(f"[{index}/{total}]")
            print(f"Request:  {request}")
            print(f"Expected: {expected}")
            print(f"Selected: {selected}")
            print(f"Result:   {result_text}")
            print("-" * 50)

        # =========================================
        # Overall metrics
        # =========================================

        accuracy = (
            correct / total * 100
            if total
            else 0
        )

        successful_tool_calls = (
            total - tool_call_failures
        )

        reliability = (
            successful_tool_calls / total * 100
            if total
            else 0
        )

        print(
            "\n========== OVERALL SUMMARY =========="
        )

        print(
            f"Total tests:          {total}"
        )

        print(
            f"Correct tools:        {correct}"
        )

        print(
            f"Wrong tools:          {wrong}"
        )

        print(
            f"Tool-call failures:   {tool_call_failures}"
        )

        print(
            f"No tool selected:     {no_tool_selected}"
        )

        print(
            f"Accuracy:             {accuracy:.2f}%"
        )

        print(
            f"Tool-call reliability:{reliability:.2f}%"
        )

        # =========================================
        # Per-tool metrics
        # =========================================

        print(
            "\n========== PER-TOOL ACCURACY =========="
        )

        for tool_name, data in stats.items():

            if data["total"] == 0:
                continue

            tool_accuracy = (
                data["correct"]
                / data["total"]
                * 100
            )

            print(
                f"{tool_name:<25}"
                f"{tool_accuracy:>7.2f}%   "
                f"({data['correct']}/"
                f"{data['total']})"
            )

        # =========================================
        # Wrong cases
        # =========================================

        if wrong_cases:

            print(
                "\n========== WRONG TOOL CASES =========="
            )

            for case in wrong_cases:

                print(
                    f"Request:  {case['request']}"
                )

                print(
                    f"Expected: {case['expected']}"
                )

                print(
                    f"Selected: {case['selected']}"
                )

                print("-" * 50)

        # =========================================
        # Tool-call failures
        # =========================================

        if failure_cases:

            print(
                "\n========== TOOL-CALL FAILURES =========="
            )

            for case in failure_cases:

                print(
                    f"Request:  {case['request']}"
                )

                print(
                    f"Expected: {case['expected']}"
                )

                print(
                    "Reason:   Model/API tool-call failure"
                )

                print("-" * 50)


if __name__ == "__main__":
    asyncio.run(run())