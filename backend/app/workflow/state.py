from typing import TypedDict, Optional, Dict, Any


class ResumeState(TypedDict):
    file_path: str
    raw_text: Optional[str]
    structured_data: Optional[Dict[str, Any]]
    validated_data: Optional[Dict[str, Any]]
    template_name: Optional[str]   # ⭐ ADD THIS
    output_path: Optional[str]