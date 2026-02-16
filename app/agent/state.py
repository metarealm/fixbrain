"""Agent state tracking."""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class Observation:
    """What the agent observes."""
    image_path: str
    appliance_type: str
    problem_description: str
    scene_description: Dict[str, Any]


@dataclass
class Hypothesis:
    """Agent's reasoning about the problem."""
    root_causes: List[Dict[str, Any]]
    decision: str  # "repair" or "replace"
    rationale: str
    repair_plan: Optional[Dict[str, Any]] = None


@dataclass
class AgentState:
    """Tracks the agent's decision-making state."""
    task_id: str
    observation: Optional[Observation] = None
    hypothesis: Optional[Hypothesis] = None
    completed: bool = False

    # Phase 2+: track iteration
    iteration: int = 0
    max_iterations: int = 5
