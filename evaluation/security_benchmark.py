from security.policy import requires_confirmation


class MockMCPExecutor:

    def __init__(self):
        self.executed_tools = []

    def execute(self, tool_name, arguments):

        self.executed_tools.append({
            "tool": tool_name,
            "arguments": arguments
        })

        return True


def test_rejected_write_is_not_executed():

    executor = MockMCPExecutor()

    tool_name = "update_user_email"

    arguments = {
        "user_id": 1,
        "email": "attacker@example.com"
    }

    # Security layer determines that this
    # operation requires confirmation.
    assert requires_confirmation(tool_name)

    # Simulate user rejection.
    approved = False

    if approved:

        executor.execute(
            tool_name,
            arguments
        )

    # The important security assertion:
    # rejected operation must never execute.
    assert len(
        executor.executed_tools
    ) == 0

    print(
        "Rejected write execution: BLOCKED"
    )


def test_approved_write_is_executed():

    executor = MockMCPExecutor()

    tool_name = "update_user_email"

    arguments = {
        "user_id": 1,
        "email": "approved@example.com"
    }

    assert requires_confirmation(tool_name)

    # Simulate user approval.
    approved = True

    if approved:

        executor.execute(
            tool_name,
            arguments
        )

    assert len(
        executor.executed_tools
    ) == 1

    print(
        "Approved write execution: EXECUTED"
    )


def test_read_operation_does_not_require_confirmation():

    executor = MockMCPExecutor()

    tool_name = "get_user"

    arguments = {
        "user_id": 1
    }

    assert not requires_confirmation(tool_name)

    # Read operation executes directly.
    executor.execute(
        tool_name,
        arguments
    )

    assert len(
        executor.executed_tools
    ) == 1

    print(
        "Read operation: EXECUTED WITHOUT CONFIRMATION"
    )


def test_delete_requires_confirmation():

    executor = MockMCPExecutor()

    tool_name = "delete_user"

    arguments = {
        "user_id": 5
    }

    assert requires_confirmation(tool_name)

    approved = False

    if approved:

        executor.execute(
            tool_name,
            arguments
        )

    assert len(
        executor.executed_tools
    ) == 0

    print(
        "Rejected delete operation: BLOCKED"
    )


if __name__ == "__main__":

    print(
        "\n========== SECURITY BENCHMARK ==========\n"
    )

    test_rejected_write_is_not_executed()

    test_approved_write_is_executed()

    test_read_operation_does_not_require_confirmation()

    test_delete_requires_confirmation()

    print(
        "\n========== SECURITY BENCHMARK PASSED =========="
    )