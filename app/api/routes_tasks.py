# app/api/routes_tasks.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.schemas import AnalyzeResult, RootCause, RepairPart, RepairPlan
from app.core.pipeline import run_analysis_pipeline

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/{task_id}/analyze", response_model=AnalyzeResult)
async def analyze_task(
    task_id: str,
    appliance_type: str = Form(...),
    problem_description: str = Form(...),
    image: UploadFile = File(...),
):
    """
    Endpoint called either by your Pi client or by a web UI.
    Accepts one image + metadata and returns diagnosis + plan.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    image_bytes = await image.read()

    result = run_analysis_pipeline(
        task_id=task_id,
        appliance_type=appliance_type,
        problem_description=problem_description,
        image_bytes=image_bytes,
    )

    llm = result["llm_result"]

    # Map raw llm_result dict into Pydantic AnalyzeResult
    root_causes = [
        RootCause(
            name=rc["name"],
            likelihood=rc["likelihood"],
            evidence=rc.get("evidence", []),
        )
        for rc in llm.get("root_causes", [])
    ]

    repair_dict = llm.get("repair")
    repair = None
    if repair_dict:
        parts = [
            RepairPart(
                name=p["name"],
                description=p.get("description", ""),
                critical=p.get("critical", True),
            )
            for p in repair_dict.get("parts", [])
        ]
        repair = RepairPlan(
            difficulty=repair_dict.get("difficulty", 3),
            estimated_time_minutes=repair_dict.get("estimated_time_minutes", 60),
            tools=repair_dict.get("tools", []),
            parts=parts,
            steps=repair_dict.get("steps", []),
        )

    analyze_result = AnalyzeResult(
        decision=llm.get("decision", "repair"),
        rationale=llm.get("rationale", ""),
        root_causes=root_causes,
        repair=repair,
    )

    return analyze_result

