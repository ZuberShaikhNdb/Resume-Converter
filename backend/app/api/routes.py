import os
import shutil
from fastapi import APIRouter, UploadFile, File

from app.workflow.graph import build_graph

router = APIRouter()

graph = build_graph()

UPLOAD_DIR = "app/uploads"


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    state = {
        "file_path": file_path,
        "raw_text": None,
        "structured_data": None
    }

    result = graph.invoke(state)

    return result["structured_data"]
    return {"pdf": result["output_path"]}
