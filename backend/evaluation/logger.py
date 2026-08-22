import json
import os
from datetime import datetime


LOG_FILE = "evaluation/results.jsonl"


def log_result(
    user_request: str,
    expected_tool: str,
    selected_tool: str | None,
    tool_type: str,
    confirmation_required: bool,
    confirmation_given: bool | None,
    execution_success: bool | None,
    execution_time_ms: float | None,
):
    os.makedirs(
        os.path.dirname(LOG_FILE),
        exist_ok=True
    )

    result = {
        "timestamp": datetime.now().isoformat(),

        "user_request": user_request,

        "expected_tool": expected_tool,

        "selected_tool": selected_tool,

        "tool_type": tool_type,

        "tool_selection_correct": (
            selected_tool == expected_tool
            if selected_tool is not None
            else False
        ),

        "confirmation_required": confirmation_required,

        "confirmation_given": confirmation_given,

        "execution_success": execution_success,

        "execution_time_ms": execution_time_ms,
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(result)
            + "\n"
        )