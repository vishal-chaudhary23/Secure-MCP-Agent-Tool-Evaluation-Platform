from security.confirmation import ask_confirmation


def test_confirmation_rejected():

    print(
        "\n========== CONFIRMATION REJECTION TEST ==========\n"
    )

    print(
        "Testing that a modification can be rejected."
    )

    # We will test the confirmation function manually
    result = ask_confirmation(
        "update_user_email",
        {
            "user_id": 1,
            "email": "blocked@example.com"
        }
    )

    print(
        f"\nConfirmation result: {result}"
    )

    assert result is False


if __name__ == "__main__":

    test_confirmation_rejected()

    print(
        "\n========== TEST PASSED =========="
    )