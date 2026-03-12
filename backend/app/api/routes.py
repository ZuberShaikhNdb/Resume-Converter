import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from enum import Enum
from typing import List

from app.workflow.graph import build_graph

router = APIRouter()

graph = build_graph()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Template options shown in Swagger UI
class TemplateEnum(str, Enum):
    IND = "IND"
    USA = "USA"


@router.post("/upload")
async def upload_resume(
    files: List[UploadFile] = File(...),
    template: TemplateEnum = Form(...)
):

    results = []

    for file in files:

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Workflow state
        state = {
            "file_path": file_path,
            "raw_text": None,
            "structured_data": None,
            "template_name": f"{template.value}.html"
        }

        # Run workflow
        result = graph.invoke(state)

        results.append({
            "file_name": file.filename,
            "template_used": template.value,
            "structured_data": result.get("structured_data"),
            "output_pdf": result.get("output_path")
        })

    return {
        "message": "All resumes processed successfully",
        "results": results
    }