def ask_confirmation(tool_name: str, arguments: dict) -> bool:

    
    print("\n⚠️  Confirmation required")
    print(f"Tool: {tool_name}")
    print(f"Arguments: {arguments}")

    answer = input("\nAllow this operation? (yes/no): ")

    return answer.strip().lower() in {"yes", "y"}