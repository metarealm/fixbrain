# app/api/schemas.py
from typing import List, Literal, Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    appliance_type: str
    problem_description: str


class RootCause(BaseModel):
    name: str
    likelihood: float
    evidence: List[str]


class RepairPart(BaseModel):
    name: str
    description: str
    critical: bool


class RepairPlan(BaseModel):
    difficulty: int
    estimated_time_minutes: int
    tools: List[str]
    parts: List[RepairPart]
    steps: List[str]


class AnalyzeResult(BaseModel):
    decision: Literal["repair", "replace"]
    rationale: str
    root_causes: List[RootCause]
    repair: Optional[RepairPlan] = None
