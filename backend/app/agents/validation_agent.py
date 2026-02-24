def validation_agent(state):
    """
    Production-grade validation agent for Resume Converter.
    Responsibilities:
    - Schema normalization
    - Cleaning & de-duplication
    - Auto-repair of extraction mistakes
    - Downstream crash prevention
    """

    data = state.get("structured_data", {})

    # ---------- HARD FALLBACK ----------
    if not isinstance(data, dict):
        state["validated_data"] = default_schema()
        return state

    # ---------- HELPER FUNCTIONS ----------
    def clean(value):
        if isinstance(value, str):
            return value.strip()
        return ""

    def unique_preserve_order(items):
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    # ---------- BASIC FIELDS ----------
    for field in ["name", "email", "phone", "location", "summary"]:
        data[field] = clean(data.get(field))

    # ---------- SKILLS ----------
  # ---------- SKILLS ----------
    skills = data.get("skills", [])
    flat = []

    # flatten list
    if isinstance(skills, list):
        for s in skills:
            if isinstance(s, str):
                flat.extend([x.strip() for x in s.split(",")])

    flat = unique_preserve_order([x for x in flat if x])

    CATEGORY_MAP = {

        # ---------- LLM / GEN AI ----------
        "LLM & Generative AI": [
            "langchain", "pgvector", "gemini", "openai", "rag",
            "prompt", "llm", "gpt", "transformer", "ragas", "judge", "chatbot"
        ],

        # ---------- CORE AI ----------
        "AI/ML Frameworks": [
            "pytorch", "tensorflow", "scikit", "machine learning", "deep learning"
        ],

        "NLP & Text Analytics": [
            "hugging", "bert", "spacy", "nltk", "ner", "text classification"
        ],

        "Computer Vision": [
            "opencv", "yolo", "vision", "cnn", "lstm", "object detection"
        ],

        # ---------- WEB ----------
        "Frontend": [
            "react", "angular", "vue", "html", "css", "javascript", "next", "redux"
        ],

        "Backend & APIs": [
            "node", "spring", "django", "fastapi", "flask", "express", "api", "backend"
        ],

        # ---------- DATA ----------
        "Databases & Data": [
            "sql", "mysql", "mongo", "postgres", "oracle", "pandas", "numpy", "database"
        ],

        "Visualization & Analytics": [
            "power bi", "tableau", "visualization", "analysis", "monitoring"
        ],

        # ---------- INFRA ----------
        "Cloud": [
            "aws", "azure", "gcp", "vertex", "cloud"
        ],

        "DevOps": [
            "docker", "kubernetes", "ci", "cd", "jenkins", "terraform"
        ],

        # ---------- TOOLS ----------
        "Developer Tools": [
            "git", "jira", "postman", "vscode", "eclipse", "intellij"
        ],

        # ---------- SOFT ----------
        "Soft Skills": [
            "communication", "leadership", "teamwork", "adaptability", "collaboration"
        ]
    }

    categories = {}

    for skill in flat:
        assigned = False
        s = skill.lower()

        for cat, keywords in CATEGORY_MAP.items():
            if any(k in s for k in keywords):
                categories.setdefault(cat, []).append(skill)
                assigned = True
                break

        if not assigned:
            categories.setdefault("Other", []).append(skill)

    data["skills"] = [
        {"category": k, "items": v}
        for k, v in categories.items()
    ]

    # ---------- EXPERIENCE ----------
    exp = data.get("experience", [])
    cleaned_exp = []

    if isinstance(exp, list):
        for e in exp:
            if not isinstance(e, dict):
                continue

            role = clean(e.get("role"))
            company = clean(e.get("company"))
            duration = clean(e.get("duration"))

            desc = e.get("description", [])

            # normalize description
            if isinstance(desc, str):
                desc = [desc]

            if isinstance(desc, list):
                desc = [
                    clean(d)
                    for d in desc
                    if isinstance(d, str)
                    and clean(d)
                    and len(clean(d)) < 300
                ]
            else:
                desc = []

            # ---------- AUTO REPAIR ----------
            if not role and desc:
                role = "Project"

            # remove empty entries
            if role or desc:
                cleaned_exp.append({
                    "company": company,
                    "role": role,
                    "duration": duration,
                    "description": desc
                })

    # ensure at least one object exists
    if not cleaned_exp:
        cleaned_exp = [{
            "company": "",
            "role": "",
            "duration": "",
            "description": []
        }]

    data["experience"] = cleaned_exp

    # ---------- EDUCATION ----------
    edu = data.get("education", [])
    cleaned_edu = []

    if isinstance(edu, list):
        for e in edu:
            if not isinstance(e, dict):
                continue

            degree = clean(e.get("degree"))
            institute = clean(e.get("institute"))
            year = clean(e.get("year"))

            # auto-repair: if degree exists but rest empty → keep
            if degree or institute or year:
                cleaned_edu.append({
                    "degree": degree,
                    "institute": institute,
                    "year": year
                })

    if not cleaned_edu:
        cleaned_edu = [{
            "degree": "",
            "institute": "",
            "year": ""
        }]

    data["education"] = cleaned_edu

    # ---------- FINAL SAFETY ----------
    state["validated_data"] = data
    return state


# ---------- DEFAULT SCHEMA ----------
def default_schema():
    return {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "summary": "",
        "skills": [],
        "experience": [{
            "company": "",
            "role": "",
            "duration": "",
            "description": []
        }],
        "education": [{
            "degree": "",
            "institute": "",
            "year": ""
        }]
    }