import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default model
DEFAULT_MODEL = "gpt-4o-mini"


# Supported languages
LANGUAGES = [
    "English",
    "Urdu",
]


# Gender options
GENDER_OPTIONS = [
    "Male",
    "Female",
    "Other",
    "Prefer not to say",
]


# Common symptoms
SYMPTOM_OPTIONS = [
    "Fever",
    "Cough",
    "Sore throat",
    "Runny nose",
    "Headache",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Abdominal pain",
    "Chest pain",
    "Shortness of breath",
    "Dizziness",
    "Body aches",
]

