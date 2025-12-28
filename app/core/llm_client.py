# app/core/llm_client.py
import json
from typing import Dict, Any

from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def build_prompt(
    appliance_type: str,
    problem_description: str,
    scene_description: Dict[str, Any],
    ) -> str:
        """
        Build a single prompt that asks for:
        - root causes
        - decision (repair/replace)
        - repair plan
        in a strict JSON format.
        """
        return f"""
        You are an expert home appliance repair technician and cost optimizer.

        The user reports a problem:
        - Appliance type: {appliance_type}
        - Problem description: {problem_description}

        You are given a structured scene description from a perception system:
        ```json
        {json.dumps(scene_description, indent=2)}
        Your tasks:

        Propose 1–3 likely root causes for the problem.

        For each root cause, estimate its likelihood between 0 and 1.

        For each root cause, list brief evidence from the scene.

        Decide whether it is better to REPAIR the appliance or REPLACE it, and explain why.

        If repair seems viable, generate:

        difficulty of repair (1 to 5, where 1 is trivial, 5 is expert-level)

        estimated repair time in minutes

        list of required tools (generic names, e.g., "Phillips screwdriver")

        list of parts (generic names and short description)

        a clear, numbered list of step-by-step instructions for the repair.

        Important:

        If you recommend replacement, you may still propose a repair plan if there is a plausible but non-optimal repair.

        If you cannot determine something, make the best reasonable assumption based on typical appliance behavior.

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


def call_llm_diagnosis_and_plan(
    appliance_type: str,
    problem_description: str,
    scene_description: Dict[str, Any],
    ) -> Dict[str, Any]:
    prompt = build_prompt(appliance_type, problem_description, scene_description)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # or any GPT-4.x / o3-mini you like
        messages=[
            {"role": "system", "content": "You are a precise JSON-only responding assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    
    content = response.choices[0].message.content
    
    # Parse JSON safely
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # If model returns extra text, try to extract JSON between ```json ... ```
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = content[start : end + 1]
            data = json.loads(json_str)
        else:
            raise ValueError(f"LLM response is not valid JSON: {content}")

    return data



