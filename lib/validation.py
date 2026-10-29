"""Request validation helpers for POST /api/ask."""

from lib.config import MAX_QUESTION_LENGTH, MIN_QUESTION_LENGTH


def validate_question_payload(payload):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """

    def invalid(code, message):
        return None, {"error": code, "message": message}

    if not isinstance(payload, dict):
        return invalid("invalid_request", "Request body must be a JSON object.")

    if "question" not in payload:
        return invalid("missing_question", "The 'question' field is required.")

    question = payload["question"]
    if not isinstance(question, str):
        return invalid("invalid_question", "The 'question' field must be a string.")

    question = question.strip()
    if not question:
        return invalid("empty_question", "The 'question' field cannot be blank.")

    if len(question) < MIN_QUESTION_LENGTH:
        return invalid(
            "short_question",
            f"The 'question' field must be at least {MIN_QUESTION_LENGTH} characters long.",
        )

    if len(question) > MAX_QUESTION_LENGTH:
        return invalid(
            "long_question",
            f"The 'question' field must be {MAX_QUESTION_LENGTH} characters or fewer.",
        )

    return question, None
