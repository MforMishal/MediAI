"""
Utility functions for MediGuide AI.

This module handles:
- Cleaning LLM JSON responses
- Safe JSON parsing
- JSON structure validation
- Urgency validation
- Display helpers
"""

import json
import re


# ============================================================
# REQUIRED JSON FIELDS
# ============================================================

REQUIRED_FIELDS = [
    "summary",
    "possible_conditions",
    "urgency_level",
    "recommended_next_steps",
    "questions_for_doctor",
    "warning_signs",
]


VALID_URGENCY_LEVELS = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "EMERGENCY",
}


# ============================================================
# CLEAN LLM RESPONSE
# ============================================================

def clean_json_response(raw_response):
    """
    Remove common formatting mistakes from an LLM response.

    Handles responses such as:

        ```json
        {...}
        ```

    and:

        Here is the JSON:
        {...}
    """

    if raw_response is None:
        return ""

    text = str(raw_response).strip()

    # Remove opening JSON markdown fence
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove generic opening code fence
    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    # Remove closing code fence
    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


# ============================================================
# SAFE JSON PARSING
# ============================================================

def parse_json_safely(raw_response):
    """
    Safely parse an LLM response into a Python object.

    Returns:
        (data, None) when successful

        (None, error_message) when unsuccessful
    """

    if not raw_response:
        return None, "The AI returned an empty response."

    cleaned_response = clean_json_response(raw_response)

    try:
        data = json.loads(cleaned_response)

    except json.JSONDecodeError as error:
        return (
            None,
            f"The AI returned invalid JSON: {error}",
        )

    return data, None


# ============================================================
# VALIDATE ASSESSMENT
# ============================================================

def validate_assessment(data):
    """
    Validate the structure of the MediGuide AI response.
    """

    if not isinstance(data, dict):
        return (
            False,
            "The AI response is not a JSON object.",
        )

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if field not in data
    ]

    if missing_fields:
        return (
            False,
            "Missing required fields: "
            + ", ".join(missing_fields),
        )

    # Validate urgency
    urgency = str(
        data["urgency_level"]
    ).upper().strip()

    if urgency not in VALID_URGENCY_LEVELS:
        return (
            False,
            (
                "Invalid urgency level. "
                "Expected LOW, MEDIUM, HIGH, or EMERGENCY."
            ),
        )

    # Validate list fields
    list_fields = [
        "possible_conditions",
        "recommended_next_steps",
        "questions_for_doctor",
        "warning_signs",
    ]

    for field in list_fields:

        if not isinstance(data[field], list):
            return (
                False,
                f"'{field}' must be a list.",
            )

    # Normalize urgency
    data["urgency_level"] = urgency

    return True, None


# ============================================================
# COMPLETE PARSING PIPELINE
# ============================================================

def parse_and_validate_assessment(raw_response):
    """
    Clean, parse, and validate an LLM assessment.

    This is the main helper that app.py should use.
    """

    data, parse_error = parse_json_safely(
        raw_response
    )

    if parse_error:
        return None, parse_error

    valid, validation_error = validate_assessment(
        data
    )

    if not valid:
        return None, validation_error

    return data, None


# ============================================================
# EXTRACT LLM TEXT
# ============================================================

def extract_text_from_result(result):
    """
    Extract generated text from an LLMChain result.

    LLMChain may return a dictionary containing the
    generated output under 'text'.
    """

    if isinstance(result, str):
        return result

    if isinstance(result, dict):
        if "text" in result:
            return result["text"]

        # Fallback: find the first string value
        for value in result.values():
            if isinstance(value, str):
                return value

    return str(result)


# ============================================================
# URGENCY HELPERS
# ============================================================

def get_urgency_message(urgency):
    """
    Return a human-readable message for the urgency level.
    """

    messages = {
        "LOW": (
            "The information provided does not appear "
            "immediately urgent based on the limited information."
        ),

        "MEDIUM": (
            "Consider contacting a healthcare professional, "
            "especially if symptoms persist or worsen."
        ),

        "HIGH": (
            "Prompt professional medical evaluation is recommended."
        ),

        "EMERGENCY": (
            "Seek emergency medical help immediately."
        ),
    }

    return messages.get(
        urgency,
        "Consult a qualified healthcare professional."
    )


def is_emergency(urgency):
    """
    Check whether the urgency level is EMERGENCY.
    """

    return urgency == "EMERGENCY"

