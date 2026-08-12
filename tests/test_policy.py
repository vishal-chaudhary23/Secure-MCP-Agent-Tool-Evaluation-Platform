from security.policy import requires_confirmation


print(
    "get_user:",
    requires_confirmation("get_user")
)

print(
    "update_user_email:",
    requires_confirmation("update_user_email")
)

print(
    "delete_user:",
    requires_confirmation("delete_user")
)

print(
    "unknown_tool:",
    requires_confirmation("unknown_tool")
)