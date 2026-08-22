# from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP
from agent.db import get_db_connection
import re



mcp = FastMCP("User Management Server")


# Read Only Tools

# =========================================================
# READ-ONLY TOOLS
# =========================================================

@mcp.tool
def get_user(user_id: int) -> dict:
    """Get a user by ID."""

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, name, email, role, status, created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return {
                "success": False,
                "error": "User not found"
            }

        return {
            "success": True,
            "user": user
        }

    finally:
        cursor.close()
        connection.close()


@mcp.tool
def list_users() -> list:
    """List all users."""

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, name, email, role, status, created_at
            FROM users
            ORDER BY id
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


@mcp.tool
def get_user_roles(user_id: int) -> dict:
    """Get the role of a user."""

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, name, role
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return {
                "success": False,
                "error": "User not found"
            }

        return {
            "success": True,
            "user": user
        }

    finally:
        cursor.close()
        connection.close()


# =========================================================
# MODIFICATION TOOLS
# =========================================================

@mcp.tool
def update_user_email(user_id: int, email: str) -> dict:
    """Update a user's email address. This is a modification operation."""

    email = email.strip()

    # Remove Markdown mailto links if the model generates them
    match = re.search(
        r'(?:mailto:)?([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})',
        email
    )

    if not match:
        return {
            "success": False,
            "error": "Invalid email address"
        }

    email = match.group(1)

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET email = %s
            WHERE id = %s
            """,
            (email, user_id)
        )

        if cursor.rowcount == 0:
            return {
                "success": False,
                "error": "User not found"
            }

        connection.commit()

        return {
            "success": True,
            "message": f"Email updated successfully for user {user_id}"
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:
        cursor.close()
        connection.close()

@mcp.tool
def change_user_role(user_id: int, role: str) -> dict:
    """Change a user's role. This is a modification operation."""

    allowed_roles = {
        "user",
        "admin",
        "manager"
    }

    if role not in allowed_roles:
        return {
            "success": False,
            "error": f"Invalid role. Allowed roles: {list(allowed_roles)}"
        }

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET role = %s
            WHERE id = %s
            """,
            (role, user_id)
        )

        if cursor.rowcount == 0:
            return {
                "success": False,
                "error": "User not found"
            }

        connection.commit()

        return {
            "success": True,
            "message": f"User {user_id} role changed to {role}"
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:
        cursor.close()
        connection.close()


@mcp.tool
def delete_user(user_id: int) -> dict:
    """Delete a user. This is a high-risk modification operation."""

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        if cursor.rowcount == 0:
            return {
                "success": False,
                "error": "User not found"
            }

        connection.commit()

        return {
            "success": True,
            "message": f"User {user_id} deleted successfully"
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:
        cursor.close()
        connection.close()


# =========================================================
# START MCP SERVER
# =========================================================

if __name__ == "__main__":
    mcp.run()