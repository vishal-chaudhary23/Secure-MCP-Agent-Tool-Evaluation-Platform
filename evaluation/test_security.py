from security.policy import requires_confirmation


def test_read_tools_do_not_require_confirmation():

    read_tools = [
        "get_user",
        "list_users",
        "get_user_roles",
    ]

    for tool in read_tools:

        result = requires_confirmation(tool)

        print(
            f"{tool:<25} "
            f"Confirmation required: {result}"
        )

        assert result is False


def test_write_tools_require_confirmation():

    write_tools = [
        "update_user_email",
        "change_user_role",
        "delete_user",
    ]

    for tool in write_tools:

        result = requires_confirmation(tool)

        print(
            f"{tool:<25} "
            f"Confirmation required: {result}"
        )

        assert result is True


def test_unknown_tool_requires_confirmation():

    result = requires_confirmation(
        "unknown_tool"
    )

    print(
        f"{'unknown_tool':<25} "
        f"Confirmation required: {result}"
    )

    assert result is True


if __name__ == "__main__":

    print(
        "\n========== SECURITY POLICY EVALUATION ==========\n"
    )

    test_read_tools_do_not_require_confirmation()

    print()

    test_write_tools_require_confirmation()

    print()

    test_unknown_tool_requires_confirmation()

    print(
        "\n========== ALL SECURITY TESTS PASSED =========="
    )