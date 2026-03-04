import os
import shutil
from fastapi import APIRouter, UploadFile, File
from typing import List

from app.workflow.graph import build_graph

router = APIRouter()

graph = build_graph()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_resume(files: List[UploadFile] = File(...)):

    results = []

    for file in files:

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        state = {
            "file_path": file_path,
            "raw_text": None,
            "structured_data": None
        }

        result = graph.invoke(state)

        results.append({
            "file_name": file.filename,
            "structured_data": result.get("structured_data"),
            "output_pdf": result.get("output_path")
        })

    return {
        "message": "All resumes processed successfully",
        "results": results
    }