from datetime import datetime
import re


def parse_date(date_str):
    """
    Supports:
    - Aug 2022
    - January 2022
    - 07/2022
    - 7/2022
    - 21/09/2023
    """

    date_str = date_str.strip()

    # Format: DD/MM/YYYY
    if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", date_str):
        return datetime.strptime(date_str, "%d/%m/%Y")

    # Format: MM/YYYY
    if re.match(r"^\d{1,2}/\d{4}$", date_str):
        return datetime.strptime(date_str, "%m/%Y")

    # Format: Aug 2022
    try:
        return datetime.strptime(date_str, "%b %Y")
    except:
        pass

    # Format: January 2022
    try:
        return datetime.strptime(date_str, "%B %Y")
    except:
        pass

    return None

def calculate_duration(duration_str):
    """
    Converts:
    - Aug 2022 – Jan 2024
    - 07/2022 – 01/2024
    Into:
    (1 year 5 months)
    """

    if not duration_str:
        return ""

    try:
        duration_str = duration_str.replace("–", "-").replace("—", "-")
        parts = [p.strip() for p in duration_str.split("-")]

        if len(parts) != 2:
            return ""

        start_str, end_str = parts

        start_date = parse_date(start_str)

        # Handle Present / Till Date
        if re.search(r"present|till|current", end_str, re.IGNORECASE):
            end_date = datetime.today()
        else:
            end_date = parse_date(end_str)

        if not start_date or not end_date:
            return ""

        total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        if total_months < 0:
            return ""

        years = total_months // 12
        months = total_months % 12

        result = []
        if years > 0:
            result.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            result.append(f"{months} month{'s' if months > 1 else ''}")

        return f" ({' '.join(result)})"

    except Exception:
        return ""

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
    for field in ["name", "email", "phone", "location", "summary", "total_experience"]:
        data[field] = clean(data.get(field))

    # ---------- OPTIONAL SECTIONS ----------
    optional_sections = [
        "certifications",
        "achievements",
        "projects",
        "publications",
        "domain_expertise"
    ]

    for section in optional_sections:
        value = data.get(section, [])
        if isinstance(value, list):
            data[section] = [clean(v) for v in value if clean(v)]
        else:
            data[section] = []

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
            "react", "angular", "vue", "html", "css", "javascript",
            "next", "redux", "jquery", "ajax", "xhtml", "xml", "json"
        ],

        "Backend & APIs": [
            "node", "spring", "django", "fastapi", "flask",
            "express", "api", "backend", "rest", "restful", "soap"
        ],

    # ---------- DATABASE ----------
        "Databases & Data": [
            "sql", "mysql", "mongo", "postgres", "postgresql",
            "oracle", "mariadb", "pl/sql", "sql server",
            "dynamodb", "nosql", "cassandra", "hive",
            "pig", "map reduce", "pandas", "numpy", "database", "Dynamo DB"
        ],

        "Visualization & Analytics": [
            "power bi", "tableau", "visualization", "analysis", "monitoring"
        ],

    # ---------- INFRA ----------
        "Cloud": [
            "aws", "azure", "gcp", "vertex", "cloud",
            "ec2", "lambda", "ecs", "eks", "elastic beanstalk",
            "s3", "ebs", "efs", "glacier", "rds",
            "aurora", "elasticache", "redshift", "vpc",
            "route 53", "cloudfront", "direct connect",
            "api gateway", "iam", "cognito", "kms",
            "cloudwatch", "cloudtrail", "config",
            "sage maker", "rekognition", "athena",
            "glue", "emr", "kinesis", "iot analytics"
        ],

        "DevOps": [
            "docker", "kubernetes", "ci", "cd",
            "jenkins", "terraform",
            "apache maven", "apache ant", "apache spark",
            "gnu", "winscp", "putty", "tfs"
        ],

        # ---------- TOOLS ----------
        "Developer Tools": [
            "git", "github", "jira", "postman",
            "vscode", "eclipse", "intellij",
            "pycharm", "net beans", "ms visio", "notepad++"
        ],

        # ---------- PROGRAMMING ----------
        "Programming Languages": [
            "python", "python 2", "python 3",
            "c", "c++", "java", "j2ee", "r", "unix", "pyspark"
        ],

    # ---------- OPERATING SYSTEM ----------
        "Operating Systems": [
            "linux", "windows"
        ],

    # ---------- METHODOLOGY ----------
        "Methodologies": [
            "agile", "scrum", "waterfall"
        ],

    # ---------- SOFT ----------
        "Soft Skills": [
            "communication", "leadership",
            "teamwork", "adaptability", "collaboration"
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
                duration_calc = calculate_duration(duration)
                cleaned_exp.append({
                    "company": company,
                    "role": role,
                    "duration": duration,
                    "duration_calculated": duration_calc,
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

        # ---------- AUTO TOTAL EXPERIENCE CALCULATION ----------
    total_months = 0

    for exp_item in cleaned_exp:
        duration = exp_item.get("duration", "")
        months = 0

        if duration:
            duration = duration.replace("–", "-").replace("—", "-")
            parts = [p.strip() for p in duration.split("-")]

            if len(parts) == 2:
                start_date = parse_date(parts[0])

                if re.search(r"present|till|current", parts[1], re.IGNORECASE):
                    end_date = datetime.today()
                else:
                    end_date = parse_date(parts[1])

                if start_date and end_date:
                    months = (
                        (end_date.year - start_date.year) * 12
                        + (end_date.month - start_date.month)
                    )

        total_months += max(months, 0)

    if not data.get("total_experience") and total_months > 0:
        years = total_months // 12
        months = total_months % 12

        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months > 1 else ''}")

        data["total_experience"] = " ".join(parts)

    # Ensure summary starts with experience
    total_exp = data.get("total_experience", "")
    summary = data.get("summary", "")

    if total_exp and not summary.lower().startswith(total_exp.lower()):
        data["summary"] = f"{total_exp} of experience. {summary}"

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
        "total_experience": "",
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
        }],
        "certifications": [],
        "achievements": [],
        "projects": [],
        "publications": [],
        "domain_expertise": [],
    }