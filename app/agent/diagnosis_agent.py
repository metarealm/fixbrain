"""Diagnosis Agent - orchestrates the agentic decision loop."""
from typing import Dict, Any
import os
import uuid

from app.agent.state import AgentState, Observation, Hypothesis
from app.tools import PerceptionTool, ReasoningTool, DecisionTool
from app.config import settings


class DiagnosisAgent:
    """
    Agent that diagnoses appliance problems through an agentic loop.

    Flow:
        1. OBSERVE - Gather information (image, problem description)
        2. REASON - Analyze and form hypotheses
        3. DECIDE - Make repair/replace decision
        4. ACT - Return result (Phase 2+: request more info, iterate)
    """

    def __init__(self):
        self.perception_tool = PerceptionTool()
        self.reasoning_tool = ReasoningTool()
        self.decision_tool = DecisionTool()

    def run(
        self,
        task_id: str,
        appliance_type: str,
        problem_description: str,
        image_bytes: bytes,
    ) -> Dict[str, Any]:
        """
        Execute the diagnosis agent.

        Args:
            task_id: Unique task identifier
            appliance_type: Type of appliance
            problem_description: User's problem description
            image_bytes: Image data

        Returns:
            Complete diagnosis result with decision and repair plan
        """
        # Initialize agent state
        state = AgentState(task_id=task_id)

        # 1. OBSERVE
        observation = self._observe(appliance_type, problem_description, image_bytes)
        state.observation = observation

        # 2. REASON
        hypothesis = self._reason(observation)
        state.hypothesis = hypothesis

        # 3. DECIDE
        decision = self._decide(hypothesis)

        # 4. ACT (Phase 1: just return. Phase 2+: might iterate)
        state.completed = True

        # Return full result
        return {
            "task_id": task_id,
            "appliance_type": appliance_type,
            "problem_description": problem_description,
            "image_path": observation.image_path,
            "scene": observation.scene_description,
            "llm_result": decision,
        }

    def _observe(
        self,
        appliance_type: str,
        problem_description: str,
        image_bytes: bytes,
    ) -> Observation:
        """
        OBSERVE: Gather information about the problem.

        Uses perception tool to analyze the image.
        """
        # Save image
        image_path = self._save_image(image_bytes)

        # Run perception tool
        scene_description = self.perception_tool.run(
            image_path=image_path,
            appliance_type=appliance_type,
        )

        return Observation(
            image_path=image_path,
            appliance_type=appliance_type,
            problem_description=problem_description,
            scene_description=scene_description,
        )

    def _reason(self, observation: Observation) -> Hypothesis:
        """
        REASON: Analyze the observation and form hypotheses.

        Uses reasoning tool (LLM) to generate root causes and plans.
        """
        reasoning_output = self.reasoning_tool.run(
            appliance_type=observation.appliance_type,
            problem_description=observation.problem_description,
            scene_description=observation.scene_description,
        )

        return Hypothesis(
            root_causes=reasoning_output.get("root_causes", []),
            decision=reasoning_output.get("decision", "repair"),
            rationale=reasoning_output.get("rationale", ""),
            repair_plan=reasoning_output.get("repair"),
        )

    def _decide(self, hypothesis: Hypothesis) -> Dict[str, Any]:
        """
        DECIDE: Make final decision based on hypotheses.

        Uses decision tool to apply business logic.
        """
        reasoning_output = {
            "root_causes": hypothesis.root_causes,
            "decision": hypothesis.decision,
            "rationale": hypothesis.rationale,
            "repair": hypothesis.repair_plan,
        }

        return self.decision_tool.run(reasoning_output)

    def _save_image(self, image_bytes: bytes) -> str:
        """Save image to disk and return path."""
        os.makedirs(os.path.join(settings.data_dir, "images"), exist_ok=True)

        image_id = f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(settings.data_dir, "images", image_id)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        return image_path
