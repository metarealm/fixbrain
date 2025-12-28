# app/core/perception.py
from typing import Dict


def run_perception(image_path: str, appliance_type: str) -> Dict:
    """
    Stub perception. Replace later with YOLO / depth, etc.
    Return a minimal scene description that LLM can use.
    """
    # TODO: run YOLO here and build real object list
    # For now we return a dummy structure.
    scene = {
        "appliance": appliance_type,
        "objects": [
            {
                "label": "pipe",
                "confidence": 0.8,
                "bbox": [100, 120, 200, 260],
            }
        ],
        "notes": [
            "Perception is stubbed; this is placeholder data."
        ],
    }
    return scene
