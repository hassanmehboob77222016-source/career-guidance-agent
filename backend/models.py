from pydantic import BaseModel, Field
from typing import List, Optional

class StudentProfile(BaseModel):
    fsc_marks: str = Field(description="The student's marks or percentage in FSC (e.g., '85%', '900/1100')")
    fsc_group: str = Field(description="The student's FSC group (e.g., Pre-Engineering, Pre-Medical, ICS)")
    interests: str = Field(description="The student's personal interests and hobbies")
    city: Optional[str] = Field(default="Any", description="Preferred city for university")

class CareerPath(BaseModel):
    title: str
    description: str
    skills_required: List[str]

class University(BaseModel):
    name: str
    programs: List[str]
    estimated_fee: str
    merit_info: str

class Scholarship(BaseModel):
    name: str
    description: str
    eligibility: str
    link: Optional[str] = None

class FreeCourse(BaseModel):
    title: str
    platform: str
    link: str

class GuidanceResponse(BaseModel):
    career_paths: List[CareerPath]
    universities: List[University]
    scholarships: List[Scholarship]
    free_courses: List[FreeCourse]
    roadmap_summary: str
