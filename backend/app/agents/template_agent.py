from app.template.template_service import generate_resume
import os


def template_agent(state):
    data = state["validated_data"]

    file_path = state["file_path"]
    filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(filename)[0]

    output_path = f"app/uploads/{name_without_ext}_converted.pdf"

    path = generate_resume(data, output_path=output_path)

    state["output_path"] = path

    return state