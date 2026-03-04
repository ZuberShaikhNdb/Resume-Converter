import os
import json
import re
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def clean_json(text: str):
    """Remove markdown formatting from LLM output"""
    text = text.strip()
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


def extract_total_experience_fallback(raw_text: str):
    """
    Fallback regex method to extract total experience
    if LLM fails to return it.
    """
    patterns = [
        r"(\d+\+?\s+years?\s+of\s+experience)",
        r"(\d+\+?\s+yrs?\s+experience)",
        r"(\d+\+?\s+years?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            return match.group(1)

    return ""


def extraction_agent(state):
    raw_text = state["raw_text"]

    prompt = f"""
    You are an expert resume parser.

    Convert the resume into STRICT JSON using EXACT schema below.

    SCHEMA:
    {{
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "total_experience": "",
        "summary": "",
        "skills": [],
        "experience": [
            {{
                "company": "",
                "role": "",
                "duration": "",
                "description": []
            }}
        ],
        "education": [
            {{
                "degree": "",
                "institute": "",
                "year": ""
            }}
        ],
        "certifications": [],
        "achievements": [],
        "projects": [],
        "publications": [],
        "domain_expertise": []
    }}

    RULES:
    - Extract total years of experience clearly (example: "5+ years")
    - The summary MUST begin with total years of experience if available
    - DO NOT remove years of experience from summary
    - Map Projects → experience
    - Use project name as role
    - Extract institute + year from education
    - Return ONLY JSON

    Resume:
    {raw_text}
    """

    response = model.generate_content(prompt)
    output = response.text
    cleaned = clean_json(output)

    try:
        structured_data = json.loads(cleaned)
    except Exception as e:
        state["structured_data"] = {"error": str(e), "raw": cleaned}
        return state

    # 🔥 VALIDATION + FALLBACK FIX
    # If total_experience missing → try regex extraction
    if not structured_data.get("total_experience"):
        fallback_exp = extract_total_experience_fallback(raw_text)
        structured_data["total_experience"] = fallback_exp

    # If summary does not start with experience → prepend it
    total_exp = structured_data.get("total_experience", "").strip()
    summary = structured_data.get("summary", "").strip()

    if total_exp and not summary.lower().startswith(total_exp.lower()):
        structured_data["summary"] = f"{total_exp} of experience. {summary}"

    state["structured_data"] = structured_data

    return state