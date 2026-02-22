
import os
import json
import re
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def clean_json(text: str):
    """Remove markdown formatting from LLM output"""
    text = text.strip()

    # Remove ```json and ```
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    return text.strip()


def extraction_agent(state):
    raw_text = state["raw_text"]

    prompt = f"""
    You are a resume parser.

    Convert this resume text into VALID JSON.

    Fields:
    name, email, phone, location, summary,
    skills (list),
    experience (list),
    education (list)

    IMPORTANT:
    - Return ONLY JSON
    - Do NOT use markdown
    - Do NOT wrap in ```json

    Resume:
    {raw_text}
    """

    response = model.generate_content(prompt)

    output = response.text

    cleaned = clean_json(output)

    try:
        state["structured_data"] = json.loads(cleaned)
    except Exception as e:
        state["structured_data"] = {"error": str(e), "raw": cleaned}

    return state
