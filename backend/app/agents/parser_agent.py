import pdfplumber
import docx


def parse_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def parse_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def parser_agent(state):
    file_path = state["file_path"]

    if file_path.endswith(".pdf"):
        text = parse_pdf(file_path)

    elif file_path.endswith(".docx"):
        text = parse_docx(file_path)

    else:
        raise ValueError("Unsupported file")

    state["raw_text"] = text

    return state
