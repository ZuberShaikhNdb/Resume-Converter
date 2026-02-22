def validation_agent(state):
    data = state.get("structured_data", {})

    if not isinstance(data, dict):
        state["validated_data"] = {}
        return state

    # ---------- BASIC FIELD CLEANING ----------
    data["name"] = data.get("name", "").strip()
    data["email"] = data.get("email", "").strip()
    data["phone"] = data.get("phone", "").strip()
    data["location"] = data.get("location", "").strip()
    data["summary"] = data.get("summary", "").strip()

    # ---------- SKILL CLEANING ----------
    skills = data.get("skills", [])
    if isinstance(skills, list):
        cleaned_skills = list(set([s.strip() for s in skills if s]))
        data["skills"] = cleaned_skills
    else:
        data["skills"] = []

    # ---------- EXPERIENCE CLEANING ----------
    exp = data.get("experience", [])
    if not isinstance(exp, list):
        exp = []

    cleaned_exp = []
    for e in exp:
        if isinstance(e, dict):
            cleaned_exp.append({
                "company": e.get("company", ""),
                "role": e.get("role", ""),
                "duration": e.get("duration", ""),
                "description": e.get("description", "")
            })

    data["experience"] = cleaned_exp

    # ---------- EDUCATION CLEANING ----------
    edu = data.get("education", [])
    if not isinstance(edu, list):
        edu = []

    cleaned_edu = []
    for e in edu:
        if isinstance(e, dict):
            cleaned_edu.append({
                "degree": e.get("degree", ""),
                "institute": e.get("institute", ""),
                "year": e.get("year", "")
            })

    data["education"] = cleaned_edu

    state["validated_data"] = data

    return state
