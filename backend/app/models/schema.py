from pydantic import BaseModel
from typing import List, Optional


class Experience(BaseModel):
    company: Optional[str]
    role: Optional[str]
    duration: Optional[str]
    description: Optional[str]


class Education(BaseModel):
    degree: Optional[str]
    institute: Optional[str]
    year: Optional[str]


class ResumeSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]

    summary: Optional[str]

    skills: List[str] = []

    experience: List[Experience] = []
    education: List[Education] = []
