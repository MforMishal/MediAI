# MediGuide AI
deployment link : https://mediguideapp.streamlit.app/
## AI-Powered Medical Symptom Assessment and Patient Guidance Assistant

MediGuide AI is an educational AI prototype built with **Python, Streamlit, LangChain, and OpenAI**.

The application allows users to enter basic patient information and symptoms. It then uses a LangChain-powered OpenAI model to generate structured, safety-focused preliminary guidance.

> **IMPORTANT MEDICAL & SAFETY NOTICE**
>
> MediGuide AI is an educational AI prototype only.
>
> It is **NOT** a replacement for a licensed doctor, professional diagnosis, emergency services, or medical treatment.
>
> The application must never be used to make or confirm a medical diagnosis.
>
> If symptoms suggest a medical emergency, seek emergency medical help immediately.

---

## Features

* Patient age and gender input
* Multiple symptom selection
* Additional free-text symptoms
* Symptom duration
* Severity rating from 1–10
* Existing medical conditions
* Current medications
* Additional medical notes
* Multiple answer languages
* OpenAI integration through `ChatOpenAI`
* LangChain `PromptTemplate`
* LangChain `ChatPromptTemplate`
* `SystemMessage`, `HumanMessage`, and `AIMessage` demonstration
* Reusable `LLMChain`
* Structured JSON output
* Safe JSON parsing and validation
* Live streaming using `.stream()`
* Streamlit `st.write_stream()`
* In-memory caching
* SQLite persistent caching
* Urgency classification:

  * LOW
  * MEDIUM
  * HIGH
  * EMERGENCY
* Safety warnings and emergency guidance
* Structured results dashboard

The required application output includes a symptom summary, possible conditions for educational purposes, urgency level, recommended next steps, questions for a healthcare professional, and warning signs.

---

## Technology Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python 3.10+          | Programming language            |
| Streamlit             | User interface                  |
| LangChain             | LLM application framework       |
| `langchain-openai`    | OpenAI integration              |
| `langchain-community` | Caching components              |
| `langchain-core`      | Prompts and message objects     |
| OpenAI                | Language model                  |
| `python-dotenv`       | Environment variable management |
| SQLite                | Persistent cache                |

These technologies follow the assignment specification.

---

## Project Structure

```text
medical_ai_assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── chains.py
│   ├── cache_manager.py
│   └── utils.py
│
└── docs/
    └── Medical_AI_Assignment.pdf
```

### File Responsibilities

#### `app.py`

Contains the Streamlit user interface:

* Sidebar
* Patient form
* Input validation
* Cache selection
* Results dashboard
* Streaming output
* Safety warnings

#### `src/config.py`

Contains:

* Environment configuration
* OpenAI API key
* Default model
* Language options
* Gender options
* Symptom options

#### `src/prompts.py`

Contains:

* Medical system prompt
* JSON schema instructions
* `PromptTemplate`
* `ChatPromptTemplate`
* Narrative streaming prompt

#### `src/chains.py`

Contains:

* `ChatOpenAI`
* Reusable `LLMChain`
* Medical assessment function
* `SystemMessage` / `HumanMessage` / `AIMessage` demonstration
* Streaming generator

#### `src/cache_manager.py`

Contains:

* `InMemoryCache`
* `SQLiteCache`
* Cache configuration switches
* Cache descriptions

#### `src/utils.py`

Contains:

* JSON cleaning
* Safe JSON parsing
* Response validation
* Urgency helpers
* LLM response extraction

---

# Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd medical_ai_assistant
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# API Key Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

You can use `.env.example` as a template.

### Security

Never commit your real `.env` file to GitHub.

The `.gitignore` file should contain:

```gitignore
.env
.venv/
__pycache__/
*.db
*.sqlite
```

The assignment explicitly requires the API key to be loaded from `.env` and never hard-coded or committed to version control.

---

# Running the Application

From the project root:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where the application can be accessed.

---

# How It Works

The application follows this general pipeline:

```text
User Input
    │
    ▼
Streamlit Form
    │
    ▼
Build Patient Prompt
    │
    ├───────────────┐
    ▼               ▼
LLMChain         ChatPromptTemplate
    │               │
    ▼               ▼
Structured JSON   Streaming
    │               │
    ▼               ▼
Safe JSON Parser  st.write_stream()
    │
    ▼
Validation
    │
    ▼
Results Dashboard
```

---

# LangChain Implementation

## PromptTemplate

The application uses a reusable `PromptTemplate` containing patient variables:

```text
age
gender
symptoms
duration
severity
existing_conditions
medications
notes
language
```

This template is used by the reusable medical assessment chain.

---

## ChatPromptTemplate

A `ChatPromptTemplate` is used for the conversational prompt:

```text
SystemMessage
      +
HumanMessage
      ↓
ChatOpenAI
```

The system message defines the AI's role and safety constraints, while the human message contains the patient's information.

---

## Message Types

The project demonstrates:

```python
SystemMessage
HumanMessage
AIMessage
```

These represent different parts of a LangChain conversation.

---

# Structured JSON Output

The assessment model is instructed to return only valid JSON using the following structure:

```json
{
    "summary": "",
    "possible_conditions": [
        {
            "name": "",
            "reason": ""
        }
    ],
    "urgency_level": "",
    "recommended_next_steps": [],
    "questions_for_doctor": [],
    "warning_signs": []
}
```

The application validates:

* Required fields
* JSON structure
* Urgency level
* List fields

Valid urgency levels are:

```text
LOW
MEDIUM
HIGH
EMERGENCY
```

---

# Safe JSON Parsing

LLMs can occasionally return malformed JSON or surround JSON with Markdown code fences.

MediGuide AI handles this using the following process:

````text
Raw LLM response
       │
       ▼
Remove ```json fences
       │
       ▼
json.loads()
       │
       ▼
Validate structure
       │
       ▼
Safe Python dictionary
````

If parsing fails, the application does **not** crash.

Instead, it displays a friendly error and provides the raw response inside a debugging expander.

This follows the assignment's requirement that invalid JSON must never crash the application.

---

# Streaming

MediGuide AI uses the model's:

```python
llm.stream()
```

method to generate a live narrative.

The chunks are displayed using:

```python
st.write_stream()
```

This produces a natural typing-style experience rather than making the user wait for the complete narrative.

The assignment specifically requires streaming using `.stream()` and `st.write_stream()`.

---

# Caching

The application supports three cache modes.

## 1. In-memory

```text
InMemoryCache
```

Stores responses in RAM.

### Advantages

* Very fast
* Simple
* Good for a single application session

### Disadvantage

The cache disappears when the application restarts.

---

## 2. SQLite

```text
SQLiteCache
```

Stores cached responses in a local SQLite database.

### Advantages

* Persistent
* Survives application restarts
* Useful for repeated requests across sessions

### Disadvantage

Slightly slower than an in-memory cache.

---

## 3. None

Caching can also be disabled.

```text
None
```

Every model request is sent to the OpenAI API.

The assignment requires demonstrating the difference between RAM-based `InMemoryCache` and disk-based `SQLiteCache`.

---

# Medical Safety

Safety is a core part of this project.

The application:

* Clearly identifies itself as an educational AI system
* Never presents a confirmed diagnosis
* Describes possible conditions only for educational purposes
* Encourages consultation with qualified healthcare professionals
* Highlights warning signs
* Provides emergency guidance for emergency-level situations
* Does not recommend changing prescribed medication without professional advice

The assignment explicitly requires the disclaimer to appear in the sidebar, main area, and results area.

---

# Testing

The assignment specifies six main testing scenarios.

## Test 1 — Mild respiratory symptoms

```text
Age: 25
Symptoms: Runny nose + sore throat
Duration: 1-3 days
Severity: 2
```

Expected:

```text
LOW
```

The application should provide calm monitoring advice.

---

## Test 2 — Fever and cough

```text
Age: 40
Symptoms: Fever + cough
Duration: 4-7 days
Severity: 6
```

Expected:

```text
MEDIUM / HIGH
```

The application should recommend professional evaluation.

---

## Test 3 — Potential emergency

```text
Symptoms: Severe chest pain + shortness of breath
```

Expected:

```text
HIGH / EMERGENCY
```

The application should urge the user to seek immediate medical help.

---

## Test 4 — Cache

Submit exactly the same information twice with caching enabled.

Expected:

```text
First request  → API call
Second request → Cached result
```

The second request should be visibly faster.

---

## Test 5 — Empty symptoms

Submit the form without entering symptoms.

Expected:

```text
Warning displayed
No API request made
```

---

## Test 6 — Urdu

Select:

```text
Language = Urdu
```

Expected:

```text
Guidance is returned in Urdu.
```

These scenarios come directly from the assignment's testing requirements.

---

# Example Workflow

```text
1. User opens MediGuide AI
            ↓
2. Enters age and gender
            ↓
3. Selects symptoms
            ↓
4. Provides duration and severity
            ↓
5. Adds medical context
            ↓
6. Selects language
            ↓
7. Selects cache
            ↓
8. Clicks "Assess Symptoms"
            ↓
9. LangChain builds the prompt
            ↓
10. OpenAI generates structured assessment
            ↓
11. JSON is safely parsed and validated
            ↓
12. Results dashboard is displayed
            ↓
13. Human-readable guidance streams live
```

---

# Limitations

MediGuide AI is a prototype created for educational purposes.

It does not:

* Perform medical diagnosis
* Replace a physician
* Replace emergency services
* Perform physical examinations
* Access medical records
* Interpret laboratory results unless explicitly provided as text
* Guarantee medically accurate conclusions
* Provide individualized medical treatment

Users should consult qualified healthcare professionals for medical decisions.

---

# Future Improvements

Potential extensions include:

* Conversation history
* Patient session history
* PDF report generation
* Additional language support
* Dark/light mode
* Voice symptom input
* Urgency analytics dashboard
* Docker deployment

These correspond to the optional bonus features listed in the assignment.

---

# Assignment Requirements Coverage

| Requirement          | Implementation            |
| -------------------- | ------------------------- |
| Streamlit UI         | `app.py`                  |
| ChatOpenAI           | `src/chains.py`           |
| PromptTemplate       | `src/prompts.py`          |
| ChatPromptTemplate   | `src/prompts.py`          |
| SystemMessage        | `src/chains.py`           |
| HumanMessage         | `src/chains.py`           |
| AIMessage            | `src/chains.py`           |
| LLMChain             | `src/chains.py`           |
| Structured JSON      | `src/prompts.py`          |
| Safe JSON parsing    | `src/utils.py`            |
| Streaming            | `src/chains.py`           |
| `st.write_stream()`  | `app.py`                  |
| InMemoryCache        | `src/cache_manager.py`    |
| SQLiteCache          | `src/cache_manager.py`    |
| Medical disclaimer   | `app.py`                  |
| Error handling       | `src/utils.py` + `app.py` |
| Modular architecture | `src/` + `app.py`         |

---

# License

This project was developed as an educational programming assignment.

It is not a medical device and must not be used for real-world diagnosis or treatment.

```

This README covers the assignment's submission requirements as well: repository contents, working `requirements.txt`, `.env.example`, setup/run instructions, caching explanation, and documentation.
```
