READ_ONLY_TOOLS = {
    "get_user",
    "list_users",
    "get_user_roles",
}

MODIFICATION_TOOLS = {
    "update_user_email",
    "change_user_role",
    "delete_user",
}


def requires_confirmation(tool_name: str) -> bool:

    if tool_name in MODIFICATION_TOOLS:
        return True

    if tool_name in READ_ONLY_TOOLS:
        return False

    # Unknown tools should be treated as dangerous
    return True