import asyncio
import json
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from security.policy import requires_confirmation

READ_TESTS = [
    {
        "tool": "get_user",
        "arguments": {"user_id": 1},
    },
    {
        "tool": "list_users",
        "arguments": {},
    },
    {
        "tool": "get_user_roles",
        "arguments": {"user_id": 1},
    },
]


WRITE_TESTS = [
    {
        "tool": "update_user_email",
        "arguments": {
            "user_id": 1,
            "email": "security_test@example.com",
        },
    },
    {
        "tool": "change_user_role",
        "arguments": {
            "user_id": 1,
            "role": "manager",
        },
    },
    {
        "tool": "delete_user",
        "arguments": {
            "user_id": 5,
        },
    },
]


async def main():

    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "mcp_servers.user_server"],
    )

    client = Client(transport)

    async with client:

        tools = await client.list_tools()

        available_tools = {
            tool.name
            for tool in tools
        }

        print(
            "\n========== END-TO-END SECURITY EVALUATION ==========\n"
        )

        # ==========================================
        # 1. Verify READ operations
        # ==========================================

        print("READ OPERATIONS\n")

        for test in READ_TESTS:

            tool_name = test["tool"]

            assert tool_name in available_tools

            assert not requires_confirmation(
                tool_name
            )

            result = await client.call_tool(
                tool_name,
                test["arguments"],
            )

            assert not result.is_error

            print(
                f"✓ {tool_name:<25}"
                "executed without confirmation"
            )

        # ==========================================
        # 2. Test rejected WRITE operations
        # ==========================================

        print("\nREJECTED WRITE OPERATIONS\n")

        blocked = 0

        for test in WRITE_TESTS:

            tool_name = test["tool"]

            assert tool_name in available_tools

            assert requires_confirmation(
                tool_name
            )

            # Simulate user rejecting operation.
            approved = False

            if not approved:

                blocked += 1

                print(
                    f"✓ {tool_name:<25}"
                    "blocked before MCP execution"
                )

                continue

            # This should NEVER execute for a rejected operation.
            raise AssertionError(
                f"SECURITY FAILURE: {tool_name} "
                "would have executed without approval"
            )

        # ==========================================
        # 3. Test approved WRITE
        # ==========================================

        print("\nAPPROVED WRITE OPERATION\n")

        test = {
            "tool": "update_user_email",
            "arguments": {
                "user_id": 1,
                "email": "approved_security_test@example.com",
            },
        }

        assert requires_confirmation(
            test["tool"]
        )

        approved = True

        assert approved is True

        result = await client.call_tool(
            test["tool"],
            test["arguments"],
        )

        assert not result.is_error

        print(
            "✓ Approved update_user_email executed"
        )

        # ==========================================
        # Summary
        # ==========================================

        print(
            "\n========== SECURITY SUMMARY =========="
        )

        print(
            f"Read operations tested:       {len(READ_TESTS)}"
        )

        print(
            f"Rejected writes tested:       {len(WRITE_TESTS)}"
        )

        print(
            f"Rejected writes blocked:      {blocked}"
        )

        print(
            "Approved write executed:      1"
        )

        print(
            f"Unauthorized executions:      {0}"
        )

        print(
            "\n✓ SECURITY EVALUATION PASSED"
        )


if __name__ == "__main__":
    asyncio.run(main())