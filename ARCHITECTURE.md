# FixBrain Phase 1 - Architecture

## Overview

FixBrain uses a **tool-based agentic architecture** where an agent orchestrates multiple tools to diagnose appliance problems.

---

## Directory Structure

```
fixbrain/
├── app/
│   ├── agent/                      # Agent orchestration
│   │   ├── diagnosis_agent.py     # Main agent with decision loop
│   │   └── state.py               # Agent state tracking
│   │
│   ├── tools/                      # Tools the agent can use
│   │   ├── perception.py          # Vision/image analysis
│   │   ├── reasoning.py           # LLM-based reasoning
│   │   └── decisions.py           # Business logic & decisions
│   │
│   ├── api/                        # HTTP API layer
│   │   ├── routes_tasks.py        # Endpoints
│   │   └── schemas.py             # Pydantic models
│   │
│   ├── config.py                   # Configuration
│   └── main.py                     # FastAPI app
│
├── tests/
│   └── test_real.py                # Real image tests
│
├── data/
│   ├── images/                     # Stored images
│   ├── tasks/                      # Task results (JSON)
│   └── images_phase1_seed/         # Test images
│
└── run_test.sh                     # Quick test runner
```

---

## Agentic Flow

### DiagnosisAgent Decision Loop

```python
┌─────────────────────────────────────┐
│      DiagnosisAgent.run()           │
└─────────────────────────────────────┘
              ↓
    ┌─────────────────┐
    │  1. OBSERVE     │  ← PerceptionTool
    │  - Save image   │  ← Analyze scene
    │  - Get context  │
    └─────────────────┘
              ↓
    ┌─────────────────┐
    │  2. REASON      │  ← ReasoningTool (LLM)
    │  - Root causes  │  ← Generate hypotheses
    │  - Likelihood   │  ← Plan repair steps
    └─────────────────┘
              ↓
    ┌─────────────────┐
    │  3. DECIDE      │  ← DecisionTool
    │  - Apply logic  │  ← Business rules
    │  - Final call   │
    └─────────────────┘
              ↓
    ┌─────────────────┐
    │  4. ACT         │
    │  - Return plan  │  (Phase 2: iterate)
    └─────────────────┘
```

---

## Component Details

### Agent Layer

**`agent/diagnosis_agent.py`**
- Orchestrates the decision loop
- Manages agent state
- Calls tools in sequence
- Handles image storage

**`agent/state.py`**
- `AgentState`: Tracks agent's progress
- `Observation`: What the agent sees
- `Hypothesis`: What the agent thinks
- Ready for Phase 2: iteration tracking

---

### Tool Layer

Tools are **independent, reusable components** the agent can call.

**`tools/perception.py` - PerceptionTool**
- Analyzes images to extract scene information
- Currently: stub (returns placeholder data)
- Future: YOLO object detection, depth analysis

**`tools/reasoning.py` - ReasoningTool**
- Uses LLM (GPT-4o-mini) for reasoning
- Generates root causes with likelihood scores
- Creates repair plans with tools/parts/steps
- Parses structured JSON output

**`tools/decisions.py` - DecisionTool**
- Applies business logic to reasoning output
- Phase 1: Pass-through
- Phase 2+: Confidence thresholds, tool inventory checks

---

### API Layer

**`api/routes_tasks.py`**
- HTTP endpoint: `POST /tasks/{task_id}/analyze`
- Accepts: multipart form with image + metadata
- Returns: structured JSON diagnosis

**`api/schemas.py`**
- Pydantic models for validation
- `AnalyzeResult`, `RootCause`, `RepairPlan`, etc.

---

## Data Flow Example

```
User uploads image of washing machine
         ↓
API receives request
         ↓
DiagnosisAgent.run() starts
         ↓
┌──────────────────────────────────────┐
│ OBSERVE                              │
├──────────────────────────────────────┤
│ 1. Save image to data/images/        │
│ 2. PerceptionTool.run()              │
│    → scene: {appliance, objects}     │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│ REASON                               │
├──────────────────────────────────────┤
│ 1. ReasoningTool.run()               │
│    → LLM analyzes problem            │
│    → Returns root causes             │
│    → Generates repair plan           │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│ DECIDE                               │
├──────────────────────────────────────┤
│ 1. DecisionTool.run()                │
│    → Applies business rules          │
│    → Finalizes decision              │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│ ACT                                  │
├──────────────────────────────────────┤
│ 1. Save result to data/tasks/        │
│ 2. Return JSON to API                │
└──────────────────────────────────────┘
         ↓
API returns AnalyzeResult to user
```

---

## Phase 1 Capabilities

✅ **Image-based diagnosis**
- Upload appliance image
- Get structured analysis

✅ **Root cause identification**
- 1-3 likely causes
- Likelihood scores (0-1)
- Evidence from scene

✅ **Repair vs Replace decision**
- Clear recommendation
- Rationale explanation

✅ **Repair plan generation**
- Difficulty level (1-5)
- Estimated time
- Required tools list
- Required parts list
- Step-by-step instructions

✅ **Structured output**
- Valid JSON
- Pydantic validated
- Machine-readable

---

## Extension Points for Phase 2

The architecture is designed for easy extension:

### 1. Add New Tools
```python
# tools/confidence_scorer.py
class ConfidenceScorer:
    def run(self, hypothesis):
        return confidence_score
```

### 2. Add Follow-up Logic
```python
# In diagnosis_agent.py
if confidence < threshold:
    follow_ups = self._generate_follow_ups()
    return {"needs_more_info": follow_ups}
```

### 3. Add Iteration Loop
```python
# In diagnosis_agent.py
while not confident and iteration < max_iterations:
    observation = self._observe(...)
    hypothesis = self._reason(...)
    if self._is_confident(hypothesis):
        break
    iteration += 1
```

### 4. Add New MCPs/External Tools
```python
# tools/parts_lookup.py (Phase 4)
class PartsLookupTool:
    def run(self, part_name, appliance_model):
        # Query parts database
        return parts_info
```

---

## Testing

**Run all tests:**
```bash
./run_test.sh
```

**Test scenarios:**
- Washing machine drain issues
- Dishwasher spray arm problems
- Refrigerator cooling issues
- Control board failures

**Validation:**
- All 5 test cases pass
- Valid JSON output
- Sensible diagnoses
- Proper repair/replace decisions

---

## Key Design Principles

1. **Tools are independent** - Each tool can be tested/replaced separately
2. **Agent orchestrates** - Clear decision loop in one place
3. **State is explicit** - AgentState tracks progress
4. **Easy to extend** - Add tools without changing agent logic
5. **Clean separation** - Agent ≠ Tools ≠ API

---

## Phase 2 Preview

Phase 2 will add:
- **Confidence scoring** - How certain is the diagnosis?
- **Information gap detection** - What's missing?
- **Follow-up requests** - Ask for more images/info
- **Iterative reasoning** - Multi-step agent loops

The current architecture supports all of this without refactoring.

---

**Status: Phase 1 Complete ✅**

Ready to move to Phase 2.
