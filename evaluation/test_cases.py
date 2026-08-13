TEST_CASES = [

    # =========================
    # get_user
    # =========================

    {
        "request": "What is the email of user 1?",
        "expected_tool": "get_user",
    },
    {
        "request": "Tell me the details of user 2.",
        "expected_tool": "get_user",
    },
    {
        "request": "Can you show me information about user 3?",
        "expected_tool": "get_user",
    },
    {
        "request": "What is user 4's status?",
        "expected_tool": "get_user",
    },
    {
        "request": "Give me the profile of user 5.",
        "expected_tool": "get_user",
    },
    {
        "request": "Look up user 1.",
        "expected_tool": "get_user",
    },
    {
        "request": "I need the information stored for user 2.",
        "expected_tool": "get_user",
    },
    {
        "request": "What email address belongs to user 3?",
        "expected_tool": "get_user",
    },
    {
        "request": "Show me user 4's account information.",
        "expected_tool": "get_user",
    },
    {
        "request": "Retrieve user 5.",
        "expected_tool": "get_user",
    },

    # =========================
    # list_users
    # =========================

    {
        "request": "Show me all users.",
        "expected_tool": "list_users",
    },
    {
        "request": "Give me the complete user list.",
        "expected_tool": "list_users",
    },
    {
        "request": "Who are all the users?",
        "expected_tool": "list_users",
    },
    {
        "request": "List everyone in the system.",
        "expected_tool": "list_users",
    },
    {
        "request": "I want to see every registered user.",
        "expected_tool": "list_users",
    },
    {
        "request": "Display the users database.",
        "expected_tool": "list_users",
    },
    {
        "request": "Can you give me all user records?",
        "expected_tool": "list_users",
    },
    {
        "request": "How many users are currently registered?",
        "expected_tool": "list_users",
    },

    # =========================
    # get_user_roles
    # =========================

    {
        "request": "What role does user 2 have?",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "Is user 2 an admin?",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "Tell me user 3's role.",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "What permissions role does user 4 have?",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "Who is the role user 2 have?",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "Check the role assigned to user 1.",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "Does user 5 have a manager role?",
        "expected_tool": "get_user_roles",
    },
    {
        "request": "Find out what role user 3 has.",
        "expected_tool": "get_user_roles",
    },

    # =========================
    # update_user_email
    # =========================

    {
        "request": "Change user 1 email to test@example.com.",
        "expected_tool": "update_user_email",
    },
    {
        "request": "Update user 2's email to newuser@example.com.",
        "expected_tool": "update_user_email",
    },
    {
        "request": "Set user 3's email to aman@example.com.",
        "expected_tool": "update_user_email",
    },
    {
        "request": "Please change user 4's email to user4@example.com.",
        "expected_tool": "update_user_email",
    },
    {
        "request": "Update user 5's email to user5@example.com.",
        "expected_tool": "update_user_email",
    },
    {
        "request": "Change user 1's email to user1@example.com.",
        "expected_tool": "update_user_email",
    },
    {
        "request": "Replace user 2's current email with abc@example.com.",
        "expected_tool": "update_user_email",
    },

    # =========================
    # change_user_role
    # =========================

    {
        "request": "Change user 3 role to manager.",
        "expected_tool": "change_user_role",
    },
    {
        "request": "Make user 1 an admin.",
        "expected_tool": "change_user_role",
    },
    {
        "request": "Give user 2 the manager role.",
        "expected_tool": "change_user_role",
    },
    {
        "request": "Set user 4's role to user.",
        "expected_tool": "change_user_role",
    },
    {
        "request": "Promote user 3 to admin.",
        "expected_tool": "change_user_role",
    },
    {
        "request": "Change the permissions role of user 5 to manager.",
        "expected_tool": "change_user_role",
    },
    {
        "request": "I want user 1 to become a manager.",
        "expected_tool": "change_user_role",
    },

    # =========================
    # delete_user
    # =========================

    {
        "request": "Delete user 5.",
        "expected_tool": "delete_user",
    },
    {
        "request": "Remove user 4 from the system.",
        "expected_tool": "delete_user",
    },
    {
        "request": "Permanently delete account 3.",
        "expected_tool": "delete_user",
    },
    {
        "request": "I want to delete user 2.",
        "expected_tool": "delete_user",
    },
    {
        "request": "Remove user 1.",
        "expected_tool": "delete_user",
    },
    {
        "request": "Delete the account belonging to user 5.",
        "expected_tool": "delete_user",
    },
    {
        "request": "Permanently remove user 3.",
        "expected_tool": "delete_user",
    },
]