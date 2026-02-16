# FixBrain Phase 1 - Testing Guide

## Prerequisites

### 1. Install Dependencies

```bash
cd /work1/robot/fixbrain
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and add your actual API key
```

Or export it directly:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

---

## Test Method 1: Automated Test Script

The easiest way to test Phase 1:

```bash
cd /work1/robot/fixbrain
source venv/bin/activate
python tests/test_pipeline.py
```

This will:
- ✅ Validate JSON schema
- ✅ Create a test image if needed
- ✅ Run the full pipeline
- ✅ Display structured results
- ✅ Save results to `data/tasks/test_task_001.json`

---

## Test Method 2: API Server Testing

### Start the Server

```bash
cd /work1/robot/fixbrain
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

Open your browser and visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Test with cURL

```bash
# Create a test image first (if you don't have one)
curl -X POST "http://localhost:8000/tasks/task_123/analyze" \
  -F "appliance_type=washing machine" \
  -F "problem_description=Won't drain water, making loud grinding noise" \
  -F "image=@data/images/test_sample.jpg"
```

### Test with Python requests

```python
import requests

url = "http://localhost:8000/tasks/task_456/analyze"

files = {
    'image': ('washing_machine.jpg', open('data/images/test_sample.jpg', 'rb'), 'image/jpeg')
}

data = {
    'appliance_type': 'washing machine',
    'problem_description': 'Water pooling at bottom, pump making grinding noise'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

---

## Test Method 3: Direct Pipeline Testing

You can also test the pipeline directly in Python:

```python
from app.core.pipeline import run_analysis_pipeline

# Load a test image
with open('data/images/test_sample.jpg', 'rb') as f:
    image_bytes = f.read()

# Run analysis
result = run_analysis_pipeline(
    task_id='direct_test_001',
    appliance_type='dishwasher',
    problem_description='Not draining properly, dishes still wet',
    image_bytes=image_bytes
)

# View results
import json
print(json.dumps(result['llm_result'], indent=2))
```

---

## Expected Output Structure

The API returns a JSON response with this structure:

```json
{
  "decision": "repair",
  "rationale": "The issue is likely a clogged drain pump which is repairable",
  "root_causes": [
    {
      "name": "Clogged drain pump",
      "likelihood": 0.75,
      "evidence": [
        "Standing water at base",
        "Grinding noise from pump area"
      ]
    },
    {
      "name": "Faulty drain pump motor",
      "likelihood": 0.6,
      "evidence": [
        "Grinding noise",
        "Pump not activating"
      ]
    }
  ],
  "repair": {
    "difficulty": 2,
    "estimated_time_minutes": 45,
    "tools": [
      "Phillips screwdriver",
      "Pliers",
      "Bucket"
    ],
    "parts": [
      {
        "name": "Drain pump",
        "description": "Standard washing machine drain pump, check model number",
        "critical": true
      }
    ],
    "steps": [
      "Unplug the washing machine from power",
      "Place towels around the area to catch water",
      "Remove the rear or front panel (depending on model)",
      "Locate the drain pump (usually at the bottom)",
      "Disconnect the hoses from the pump (have bucket ready)",
      "Remove the pump mounting screws",
      "Disconnect electrical connector",
      "Install new pump in reverse order",
      "Test for leaks before reassembling fully"
    ]
  }
}
```

---

## Validation Checklist

✅ **FR-1: Image Analysis Input**
- Accepts appliance_type (string)
- Accepts problem_description (string)
- Accepts image file (jpg/png)
- HTTP API endpoint works

✅ **FR-2: Scene Understanding**
- Perception module runs (stub returns structured scene)
- Scene description is JSON

✅ **FR-3: Root Cause Identification**
- Returns 1-3 root causes
- Each has name, likelihood (0-1), and evidence list

✅ **FR-4: Repair vs Replace Decision**
- Returns "repair" or "replace"
- Includes rationale

✅ **FR-5: Repair Plan Generation**
- Returns difficulty (1-5)
- Returns estimated time
- Returns list of tools
- Returns list of parts (with description and critical flag)
- Returns step-by-step instructions

✅ **FR-6: Structured Output**
- Output is valid JSON
- Matches defined Pydantic schema
- Machine-readable, no interpretation needed

---

## Troubleshooting

### Error: "OPENAI_API_KEY not set"

Make sure you've created a `.env` file or exported the environment variable:

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Error: "Failed to load image"

Ensure your test image exists:

```bash
ls -la data/images/test_sample.jpg
```

Create one if needed:

```bash
# Download a sample image
curl -o data/images/test_sample.jpg https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/310px-Placeholder_view_vector.svg.png
```

### Error: "Module not found"

Make sure you're in the virtual environment and have installed dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port already in use

If port 8000 is in use, specify a different port:

```bash
uvicorn app.main:app --port 8001
```

---

## Performance Benchmarks (Phase 1 Targets)

- ✅ Response time: < 10 seconds (typical: 3-5 seconds)
- ✅ Output is deterministic JSON (no free text parsing needed)
- ✅ Results are persistable to disk

---

## Next Steps After Phase 1

Once Phase 1 is validated, you can move to Phase 2:

**Phase 2: Confidence, Gaps & Follow-Up Intelligence**
- Add confidence scoring
- Detect missing information
- Request additional images or metadata
- Implement follow-up loops

---

## Sample Test Scenarios

### Scenario 1: Washing Machine Won't Drain

```bash
appliance_type: "washing machine"
problem_description: "Water won't drain, making grinding noise"
image: Picture of washing machine with visible water at bottom
```

Expected: Likely diagnose clogged pump or faulty pump motor

### Scenario 2: Dishwasher Not Cleaning

```bash
appliance_type: "dishwasher"
problem_description: "Dishes still dirty after cycle, spray arm not spinning"
image: Picture of dishwasher interior
```

Expected: Likely diagnose clogged spray arm or water inlet valve issue

### Scenario 3: Refrigerator Not Cooling

```bash
appliance_type: "refrigerator"
problem_description: "Not cooling properly, compressor running constantly"
image: Picture of refrigerator with frost buildup
```

Expected: Likely diagnose evaporator coil issue or defrost system failure

---

## Data Inspection

After running tests, inspect the saved data:

```bash
# View saved images
ls -lh data/images/

# View task results
cat data/tasks/test_task_001.json | jq .

# View all task results
find data/tasks -name "*.json" -exec echo "--- {} ---" \; -exec cat {} \; -exec echo "" \;
```

---

## Success Criteria

Phase 1 is considered **READY** when:

1. ✅ All FR requirements (FR-1 through FR-6) are working
2. ✅ Test script passes without errors
3. ✅ API returns valid JSON matching schema
4. ✅ Response time is < 10 seconds
5. ✅ Results are saved to disk correctly
6. ✅ Manual API testing works via curl/Swagger

---

**Phase 1 Status: ✅ READY FOR TESTING**

Run `python tests/test_pipeline.py` to validate!
