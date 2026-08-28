"""
MediGuide AI
============

AI-powered medical symptom assessment and patient guidance prototype.

IMPORTANT:
This is an educational AI prototype only.
It is NOT a doctor, medical device, diagnostic system,
emergency service, or replacement for professional medical care.
"""

import streamlit as st

from src.config import (
    DEFAULT_MODEL,
    GENDER_OPTIONS,
    LANGUAGES,
    SYMPTOM_OPTIONS,
)

from src.chains import (
    run_medical_assessment,
    stream_narrative,
)

from src.cache_manager import (
    configure_cache,
    get_cache_description,
)

from src.utils import (
    extract_text_from_result,
    parse_and_validate_assessment,
    get_urgency_message,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="wide",
)


# ============================================================
# MEDICAL DISCLAIMER
# ============================================================

DISCLAIMER = """
**Medical Safety Notice**

MediGuide AI is an educational AI prototype only.

It is NOT a replacement for a licensed doctor, professional
diagnosis, emergency services, or medical treatment.

Never use this application to make a confirmed medical diagnosis.

If you believe you are experiencing a medical emergency,
seek emergency medical help immediately.
"""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("MediGuide AI")

    st.caption(
        "AI-Powered Medical Symptom Assessment "
        "and Patient Guidance Assistant"
    )

    st.divider()

    # --------------------------------------------------------
    # Model configuration
    # --------------------------------------------------------

    st.subheader("Model Configuration")

    st.write(
        f"**Model:** `{DEFAULT_MODEL}`"
    )

    openai_api_key = st.text_input(
        "OpenAI API key",
        type="password",
        key="openai_api_key",
        placeholder="sk-...",
        help="Your key is kept in this browser session and used only for your requests.",
    )

    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    st.subheader("Language")

    language = st.selectbox(
        "Answer language",
        options=LANGUAGES,
        index=0,
    )

    # --------------------------------------------------------
    # Cache
    # --------------------------------------------------------

    st.subheader("Caching")

    cache_type = st.selectbox(
        "Cache type",
        options=[
            "None",
            "In-memory",
            "SQLite",
        ],
        index=1,
    )

    st.caption(
        get_cache_description(cache_type)
    )

    # Configure selected cache
    try:
        configure_cache(cache_type)

    except Exception as error:
        st.error(
            f"Cache configuration failed: {error}"
        )

    st.divider()

# ============================================================
# MAIN AREA
# ============================================================

st.title("MediGuide AI")

st.write(
    "Enter basic patient information and symptoms to receive "
    "structured, safety-focused preliminary guidance."
)

st.error(DISCLAIMER)


# ============================================================
# PATIENT FORM
# ============================================================

with st.form("medical_assessment_form"):

    st.subheader("Patient Information")

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        age = st.text_input(
            "Age",
            placeholder="e.g 0-70",
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            options=GENDER_OPTIONS,
        )

    # --------------------------------------------------------
    # Symptoms
    # --------------------------------------------------------

    st.subheader("Symptoms")

    symptoms = st.multiselect(
        "Select symptoms",
        options=SYMPTOM_OPTIONS,
    )

    additional_symptoms = st.text_area(
        "Additional symptoms",
        placeholder="Describe any other symptoms...",
    )

    # --------------------------------------------------------
    # Duration and severity
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        duration = st.selectbox(
            "Duration of symptoms",
            options=[
                "Less than 24 hours",
                "1-3 days",
                "4-7 days",
                "1-2 weeks",
                "More than 2 weeks",
                "Unknown",
            ],
        )

    with col2:

        severity = st.slider(
            "Severity (1 = mild, 10 = severe)",
            min_value=1,
            max_value=10,
            value=5,
        )

    # --------------------------------------------------------
    # Medical context
    # --------------------------------------------------------

    st.subheader("Additional Medical Context")

    existing_conditions = st.text_area(
        "Existing medical conditions",
        placeholder="e.g. asthma, diabetes, none...",
    )

    medications = st.text_area(
        "Current medications",
        placeholder="List current medications...",
    )

    notes = st.text_area(
        "Additional notes",
        placeholder="Anything else the AI should know...",
    )

    # --------------------------------------------------------
    # Submit
    # --------------------------------------------------------

    submitted = st.form_submit_button(
        "Assess Symptoms",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# PROCESS SUBMISSION
# ============================================================

if submitted:

    # --------------------------------------------------------
    # Validate API key
    # --------------------------------------------------------

    if not openai_api_key.strip():

        st.warning(
            "Please enter your OpenAI API key in the sidebar."
        )

        st.stop()

    # --------------------------------------------------------
    # Validate symptoms
    # --------------------------------------------------------

    if not symptoms and not additional_symptoms.strip():

        st.warning(
            "Please enter or select at least one symptom."
        )

        st.stop()

    # --------------------------------------------------------
    # Validate age
    # --------------------------------------------------------

    if not age.strip():

        st.warning(
            "Please enter the patient's age."
        )

        st.stop()

    # --------------------------------------------------------
    # Combine symptoms
    # --------------------------------------------------------

    selected_symptoms = ", ".join(symptoms)

    if additional_symptoms.strip():

        if selected_symptoms:
            selected_symptoms += ", "

        selected_symptoms += (
            additional_symptoms.strip()
        )

    # --------------------------------------------------------
    # Show submitted information
    # --------------------------------------------------------

    st.subheader("Assessment")

    with st.expander(
        "View submitted patient information"
    ):

        st.write(
            f"**Age:** {age}"
        )

        st.write(
            f"**Gender:** {gender}"
        )

        st.write(
            f"**Symptoms:** {selected_symptoms}"
        )

        st.write(
            f"**Duration:** {duration}"
        )

        st.write(
            f"**Severity:** {severity}/10"
        )

        st.write(
            f"**Existing conditions:** "
            f"{existing_conditions or 'None provided'}"
        )

        st.write(
            f"**Medications:** "
            f"{medications or 'None provided'}"
        )

        st.write(
            f"**Notes:** "
            f"{notes or 'None provided'}"
        )

    # ========================================================
    # RUN STRUCTURED ASSESSMENT
    # ========================================================

    with st.spinner(
        "Analyzing the provided information..."
    ):

        try:

            result = run_medical_assessment(
                api_key=openai_api_key.strip(),
                age=age,
                gender=gender,
                symptoms=selected_symptoms,
                duration=duration,
                severity=severity,
                existing_conditions=(
                    existing_conditions or "None provided"
                ),
                medications=(
                    medications or "None provided"
                ),
                notes=(
                    notes or "None provided"
                ),
                language=language,
            )

        except Exception as error:

            st.error(
                "The assessment could not be completed."
            )

            st.exception(error)

            st.stop()

    # ========================================================
    # EXTRACT RAW RESPONSE
    # ========================================================

    raw_response = extract_text_from_result(
        result
    )

    # ========================================================
    # SAFE JSON PARSING
    # ========================================================

    assessment, error = parse_and_validate_assessment(
        raw_response
    )

    if error:

        st.error(
            "The AI response could not be safely interpreted."
        )

        st.warning(
            "No medical assessment was displayed because "
            "the response did not match the required structure."
        )

        with st.expander(
            "Raw AI response — debugging only"
        ):

            st.code(
                raw_response,
                language="text",
            )

        st.stop()

    # ========================================================
    # URGENCY
    # ========================================================

    urgency = assessment[
        "urgency_level"
    ]

    st.subheader("Urgency Level")

    if urgency == "LOW":

        st.success(
            f"LOW — {get_urgency_message(urgency)}"
        )

    elif urgency == "MEDIUM":

        st.warning(
            f"MEDIUM — {get_urgency_message(urgency)}"
        )

    elif urgency == "HIGH":

        st.error(
            f"HIGH — {get_urgency_message(urgency)}"
        )

    elif urgency == "EMERGENCY":

        st.error(
            f"EMERGENCY — {get_urgency_message(urgency)}"
        )

    # ========================================================
    # RESULTS DASHBOARD
    # ========================================================

    st.divider()

    st.subheader("Results Dashboard")

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Severity",
            f"{severity}/10",
        )

    with col2:

        st.metric(
            "Urgency",
            urgency,
        )

    # --------------------------------------------------------
    # Tabs
    # --------------------------------------------------------

    (
        summary_tab,
        conditions_tab,
        next_steps_tab,
        doctor_tab,
        warning_tab,
    ) = st.tabs(
        [
            "Summary",
            "Possible Conditions",
            "Next Steps",
            "Questions for Doctor",
            "Warning Signs",
        ]
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    with summary_tab:

        st.info(
            assessment["summary"]
        )

    # --------------------------------------------------------
    # Possible conditions
    # --------------------------------------------------------

    with conditions_tab:

        st.info(
            "These are possibilities for educational purposes "
            "only and are NOT confirmed diagnoses."
        )

        for condition in assessment[
            "possible_conditions"
        ]:

            if isinstance(condition, dict):

                name = condition.get(
                    "name",
                    "Unknown",
                )

                reason = condition.get(
                    "reason",
                    "",
                )

                st.write(
                    f"**{name}**"
                )

                if reason:
                    st.write(reason)

            else:

                st.write(
                    f"• {condition}"
                )

    # --------------------------------------------------------
    # Recommended next steps
    # --------------------------------------------------------

    with next_steps_tab:

        for step in assessment[
            "recommended_next_steps"
        ]:

            st.write(
                f"• {step}"
            )

    # --------------------------------------------------------
    # Questions for doctor
    # --------------------------------------------------------

    with doctor_tab:

        for question in assessment[
            "questions_for_doctor"
        ]:

            st.write(
                f"• {question}"
            )

    # --------------------------------------------------------
    # Warning signs
    # --------------------------------------------------------

    with warning_tab:

        if assessment["warning_signs"]:

            for warning in assessment[
                "warning_signs"
            ]:

                st.error(
                    f"• {warning}"
                )

        else:

            st.info(
                "No specific warning signs were returned. "
                "Seek medical care if symptoms worsen or "
                "you become concerned."
            )

    # ========================================================
    # STREAMING NARRATIVE
    # ========================================================

    st.divider()

    st.subheader(
        "AI Guidance"
    )

    st.caption(
        "The following guidance is streamed live from the AI."
    )

    try:

        streamed_text = st.write_stream(
            stream_narrative(
                api_key=openai_api_key.strip(),
                age=age,
                gender=gender,
                symptoms=selected_symptoms,
                duration=duration,
                severity=severity,
                existing_conditions=(
                    existing_conditions or "None provided"
                ),
                medications=(
                    medications or "None provided"
                ),
                notes=(
                    notes or "None provided"
                ),
                language=language,
            )
        )

    except Exception as error:

        st.error(
            "The live guidance stream could not be generated."
        )

        st.exception(error)

    # ========================================================
    # FINAL SAFETY WARNING
    # ========================================================

    st.divider()

    st.warning(DISCLAIMER)

    if urgency == "EMERGENCY":

        st.error(
            "EMERGENCY: Seek emergency medical help immediately."
        )

