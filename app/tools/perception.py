"""Perception tool - analyzes images to extract scene information."""
from typing import Dict, Any


class PerceptionTool:
    """Tool for extracting structured scene information from images."""

    def run(self, image_path: str, appliance_type: str) -> Dict[str, Any]:
        """
        Analyze image and return structured scene description.

        Args:
            image_path: Path to the image file
            appliance_type: Type of appliance in the image

        Returns:
            Structured scene description with detected objects
        """
        # TODO: Replace with YOLO/vision model
        # For now, return stub data
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
                "Perception is stubbed; ready for YOLO integration."
            ],
        }
        return scene
