# FixBrain Orchestrator

Short, clear answer first: **Yes.**
The agentic flow does **multi-step reasoning**, **can call tools**, and **does not rely only on an LLM**.

FixBrain is **not a chatbot** — it is a **reasoning + execution loop**.

## Agentic flow in 60 seconds

Think of FixBrain as a **planner + executor**, not a single LLM call.

Core loop:

**Observe → Reason → Decide → Act → Observe → Repeat**

## What the agent actually does (step-by-step)

### 1) Observe (non-LLM)

Uses **real tools**, not the LLM:

- Camera images (from robot or upload)
- Perception models (YOLO / OpenCV)
- Metadata (appliance type, user input)

Output: **structured scene data (JSON)**

### 2) Reason (LLM)

The LLM:

- Interprets scene + problem
- Forms hypotheses
- Decides what information is missing

Output:

- Root causes
- Confidence
- Next best action (for example: need model number, need underside view)

### 3) Decide (LLM + rules)

Decision logic combines:

- LLM output
- Hard constraints (safety, cost thresholds, tool availability)

Example:

"Repair is possible only if the user has Torx T20; otherwise recommend replacement."

### 4) Act (tools, not LLM)

Agent executes actions via **tools**:

- Request more images
- Query parts databases
- Query user tool inventory
- Run perception again
- (Later) move robot / reposition camera

The LLM does **not** do these directly — it **requests** them.

### 5) Observe again

Tool outputs come back:

- New images
- Part availability
- Tool compatibility results

Agent feeds this back into reasoning.

### 6) Final plan output

Agent produces:

- Repair vs replace decision
- Exact parts list
- Required tools
- Optimized steps based on available tools
- Cost/time estimate

## Does it do multi-step agency?

**Yes, but in a controlled way.**

Two layers:

1. **LLM = Planner**
2. **Code = Executor**

The LLM says: "I need X"

The system decides: "Can I allow X? If yes, run tool Y."

This is **safe agentic orchestration**, not autonomous chaos.

## Does it use tools beyond LLM?

**Absolutely. Most value comes from non-LLM tools.**

Tool categories:

- Perception: YOLO, OpenCV, depth analysis
- Knowledge: Manuals DB, exploded views
- Parts: Amazon, Home Depot APIs
- User state: Tool inventory DB
- Cost logic: Price comparison, thresholds
- Safety: Rule-based validators
- Robotics (later): Motion planner, gripper control

The LLM only:

- Reasons
- Plans
- Chooses actions

## Minimal agentic flow (today)

```
[Image Upload]
      ↓
[Perception Model]
      ↓
[LLM Reasoning Call]
      ↓
[Structured Repair Plan]
```

This is Agent v0.5 — and totally fine.

## Full agentic flow (next)

```
[Observe]
   ↓
[Reason]
   ↓
[Need more info?] ── yes ──> [Call Tool] ──> [Observe again]
   ↓ no
[Decide repair vs replace]
   ↓
[Validate tools + parts]
   ↓
[Final plan]
```

This is real multi-step agency.

## Why YC will like this

Because:

- You are not overengineering too early
- You are building a scalable agent loop
- Hardware is a data source, not a crutch
- The reasoning engine is the moat

One-line summary you can reuse:

"FixBrain is an agentic system that combines perception models, structured reasoning, and tool-based execution loops to diagnose, plan, and optimize real-world repairs — with LLMs acting as planners, not executors."

## How the current logic works

1. API receives a multipart request with appliance metadata and an image.
2. The pipeline saves the image to disk and runs a perception stub to produce a scene description.
3. The LLM client builds a strict JSON-only prompt using the scene + user description.
4. The model response is parsed as JSON, normalized into API schemas, and returned.
5. The full pipeline result is persisted to disk for later inspection.

Key flow and implementation points:

- Orchestration: `app/core/pipeline.py`
- Perception (stub): `app/core/perception.py`
- LLM prompt and parsing: `app/core/llm_client.py`
- HTTP endpoint: `app/api/routes_tasks.py`

## Input

Endpoint: `POST /tasks/{task_id}/analyze`

Multipart form fields:

- `appliance_type` (string)
- `problem_description` (string)
- `image` (file, must be an image content type)

## Output

JSON response shaped like `AnalyzeResult`:

- `decision`: "repair" or "replace"
- `rationale`: string
- `root_causes`: list of `{ name, likelihood, evidence[] }`
- `repair`: optional object with `{ difficulty, estimated_time_minutes, tools[], parts[], steps[] }`

Example response (truncated):

```json
{
  "decision": "repair",
  "rationale": "...",
  "root_causes": [
    {
      "name": "Clogged drain",
      "likelihood": 0.7,
      "evidence": ["Standing water near base"]
    }
  ],
  "repair": {
    "difficulty": 2,
    "estimated_time_minutes": 30,
    "tools": ["Phillips screwdriver"],
    "parts": [
      {"name": "Drain hose", "description": "Replacement hose", "critical": true}
    ],
    "steps": ["Unplug unit", "Remove rear panel", "Replace hose"]
  }
}
```

## Data persistence

The pipeline stores artifacts under `data/` by default:

- `data/images/<uuid>.jpg`
- `data/tasks/<task_id>.json` (full pipeline payload)

## Configuration

Environment variables:

- `OPENAI_API_KEY`: required for LLM calls.
- `FIXBRAIN_DATA_DIR`: optional data directory override (default: `data`).
