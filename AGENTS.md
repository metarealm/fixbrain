# Agent Notes

This repo is a small FastAPI service that orchestrates a perception + LLM pipeline for appliance diagnosis. Keep changes aligned with the existing request/response schema and pipeline flow.

## Where the logic lives
- API endpoint: `app/api/routes_tasks.py`
- Pipeline orchestration: `app/core/pipeline.py`
- Perception stub: `app/core/perception.py`
- LLM prompt + JSON parsing: `app/core/llm_client.py`
- Response models: `app/api/schemas.py`

## Invariants to preserve
- `POST /tasks/{task_id}/analyze` must accept a multipart image plus text fields.
- The LLM prompt expects a strict JSON response; parsing is tolerant but the schema should stay stable.
- `AnalyzeResult` is the public contract; update `schemas.py` and prompt together if changes are required.
- Pipeline artifacts are written under `data/` (or `FIXBRAIN_DATA_DIR`).

## Implementation tips
- Keep outputs ASCII and JSON-serializable.
- If you add new fields, update both the prompt schema and the Pydantic models.
- Avoid changing persisted file layout unless you also update any consumers.
