# FixBrain Phase 1 — Testing Preparation Plan (No Execution Yet)

Date: 2026-02-15
Scope: Prepare test data + test plan only. Do NOT run validation tests yet.

## Context reviewed
- `/work1/robot/Phases.md`
- `/work1/robot/fixbrain/doc/PHASE1_STATUS.md`
- `/work1/robot/fixbrain/doc/TESTING.md`
- `/work1/robot/fixbrain/README.md`

Phase 1 status in docs: implemented and ready for testing.

## Objective of this prep
1. Prepare realistic image inputs for Phase 1 pipeline.
2. Define a focused validation plan aligned to FR-1..FR-6.
3. Add explicit task to run dataset validation (later).

## Planned test dataset (seed)
Store generated seed images under:
- `/work1/robot/fixbrain/data/images_phase1_seed/`

Seed categories:
1. Washing machine drain failure / standing water symptoms
2. Drain pump/clog symptom close-up
3. Dishwasher spray-arm issue symptom
4. Refrigerator frost/cooling symptom
5. Appliance control-board burn/scorch symptom

## Validation checklist (to run later, not now)
For each seed image, run API analyze and verify:
- Valid JSON response schema
- Decision present (`repair|replace`)
- 1-3 root causes with likelihood/evidence
- Repair block populated when decision is `repair`
- Outputs are persisted in `data/tasks/*.json`
- Runtime and stability notes captured

## Risks to watch during actual testing
- Over-generic root causes when image signal is weak
- Overconfident recommendations with low visual evidence
- Tool/parts lists not specific enough for execution
- Inconsistent decision rationale across similar images

## Exit criteria for "prep complete"
- Seed image pack exists in data folder
- Validation task added to task board
- No tests executed yet
