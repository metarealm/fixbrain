
# app/core/pipeline.py
import os
import uuid
import json
from typing import Dict, Any

from app.config import settings
from app.core.perception import run_perception
from app.core.llm_client import call_llm_diagnosis_and_plan


def ensure_dirs():
    os.makedirs(os.path.join(settings.data_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(settings.data_dir, "tasks"), exist_ok=True)


def save_image(file_bytes: bytes, ext: str = ".jpg") -> str:
    ensure_dirs()
    image_id = f"{uuid.uuid4().hex}{ext}"
    image_path = os.path.join(settings.data_dir, "images", image_id)
    with open(image_path, "wb") as f:
        f.write(file_bytes)
    return image_path


def save_task_result(task_id: str, result: Dict[str, Any]) -> str:
    ensure_dirs()
    task_path = os.path.join(settings.data_dir, "tasks", f"{task_id}.json")
    with open(task_path, "w") as f:
        json.dump(result, f, indent=2)
    return task_path


def run_analysis_pipeline(
    task_id: str,
    appliance_type: str,
    problem_description: str,
    image_bytes: bytes,
) -> Dict[str, Any]:
    """
    End-to-end pipeline for v0:
    - save image
    - run perception
    - call LLM
    - persist result
    """
    image_path = save_image(image_bytes, ext=".jpg")

    scene = run_perception(image_path=image_path, appliance_type=appliance_type)
    llm_result = call_llm_diagnosis_and_plan(
        appliance_type=appliance_type,
        problem_description=problem_description,
        scene_description=scene,
    )

    full_result = {
        "task_id": task_id,
        "appliance_type": appliance_type,
        "problem_description": problem_description,
        "image_path": image_path,
        "scene": scene,
        "llm_result": llm_result,
    }

    save_task_result(task_id, full_result)
    return full_result

