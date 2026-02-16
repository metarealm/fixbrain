"""Reasoning tool - uses LLM to analyze problems and generate hypotheses."""
import json
from typing import Dict, Any

from openai import OpenAI
from app.config import settings


class ReasoningTool:
    """Tool for LLM-based reasoning about appliance problems."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def run(
        self,
        appliance_type: str,
        problem_description: str,
        scene_description: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Reason about the problem and generate diagnosis.

        Args:
            appliance_type: Type of appliance
            problem_description: User's problem description
            scene_description: Structured scene from perception tool

        Returns:
            Structured reasoning with root causes, decision, and repair plan
        """
        prompt = self._build_prompt(appliance_type, problem_description, scene_description)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise JSON-only responding assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content
        return self._parse_response(content)

    def _build_prompt(
        self,
        appliance_type: str,
        problem_description: str,
        scene_description: Dict[str, Any],
    ) -> str:
        """Build the reasoning prompt."""
        return f"""
You are an expert home appliance repair technician and cost optimizer.

The user reports a problem:
- Appliance type: {appliance_type}
- Problem description: {problem_description}

You are given a structured scene description from a perception system:
```json
{json.dumps(scene_description, indent=2)}
```

Your tasks:

1. Propose 1–3 likely root causes for the problem.
2. For each root cause, estimate its likelihood between 0 and 1.
3. For each root cause, list brief evidence from the scene.
4. Decide whether it is better to REPAIR the appliance or REPLACE it, and explain why.
5. If repair seems viable, generate:
   - difficulty of repair (1 to 5, where 1 is trivial, 5 is expert-level)
   - estimated repair time in minutes
   - list of required tools (generic names, e.g., "Phillips screwdriver")
   - list of parts (generic names and short description)
   - a clear, numbered list of step-by-step instructions for the repair.

Important:
- If you recommend replacement, you may still propose a repair plan if there is a plausible but non-optimal repair.
- If you cannot determine something, make the best reasonable assumption based on typical appliance behavior.

Respond ONLY with valid JSON using this exact schema:
{{
    "root_causes": [
        {{
            "name": "string",
            "likelihood": 0.0,
            "evidence": ["string"]
        }}
    ],
    "decision": "repair or replace",
    "rationale": "string",
    "repair": {{
        "difficulty": 1,
        "estimated_time_minutes": 0,
        "tools": ["string"],
        "parts": [
            {{
                "name": "string",
                "description": "string",
                "critical": true
            }}
        ],
        "steps": ["string"]
    }}
}}

Do not include any explanation outside of this JSON.
"""

    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse LLM response as JSON."""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1 and end > start:
                json_str = content[start : end + 1]
                return json.loads(json_str)
            else:
                raise ValueError(f"LLM response is not valid JSON: {content}")
