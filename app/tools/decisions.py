"""Decision tool - applies business logic to reasoning output."""
from typing import Dict, Any


class DecisionTool:
    """Tool for making final decisions based on reasoning."""

    def run(self, reasoning_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply decision logic to reasoning output.

        For Phase 1, this is pass-through. In future phases:
        - Apply cost thresholds
        - Check tool availability
        - Validate parts availability
        - Apply safety rules

        Args:
            reasoning_output: Output from reasoning tool

        Returns:
            Final decision with any business logic applied
        """
        # Phase 1: Pass through LLM decision
        # Phase 2+: Add confidence thresholds, tool checks, etc.

        decision = reasoning_output.get("decision", "repair")

        # Future: Add business rules here
        # if tool_inventory and not has_required_tools():
        #     decision = "replace"

        return {
            "decision": decision,
            "rationale": reasoning_output.get("rationale", ""),
            "root_causes": reasoning_output.get("root_causes", []),
            "repair": reasoning_output.get("repair"),
        }
