Perfect request 👍
Below are **phased, Codex-ready BRDs (Business Requirements Documents)** that are **explicitly scoped**, **testable**, and **incrementally agentic**.

These are written so that:

* Phase 1 can be built & validated **now**
* Each next phase **extends**, not rewrites
* You can literally hand **one phase at a time** to Codex

I’ll keep them concise but precise (YC + engineering friendly).

---

# 📘 FixBrain — Phased Business Requirements Documents (BRDs)

---

# **BRD – Phase 1**

## **FixBrain v0.1: Visual Diagnosis & Repair Planning (Single-Step Agent)**

### **Objective**

Build an AI system that can analyze an image of a home appliance problem and generate:

* likely root causes
* repair vs replace recommendation
* required tools
* required parts
* step-by-step repair plan

**No robotics, no autonomy, no multi-step loops yet.**

---

### **In Scope**

* Image-based problem understanding
* Structured reasoning via LLM
* Deterministic JSON output
* API-first design

---

### **Out of Scope**

* Robot navigation
* Tool inventory optimization
* Parts availability lookup
* Multi-step agent loops
* Autonomous actions

---

### **Users**

* Early internal tester (you)
* Later: home users / technicians (read-only)

---

### **Functional Requirements**

#### **FR-1 Image Analysis Input**

* System SHALL accept:

  * appliance type (string)
  * problem description (string)
  * one image (jpg/png)
* Input via HTTP API

#### **FR-2 Scene Understanding**

* System SHALL run a perception step (stub or YOLO)
* Output a structured scene description (JSON)

#### **FR-3 Root Cause Identification**

* System SHALL return 1–3 likely root causes
* Each root cause SHALL include:

  * name
  * likelihood score (0–1)
  * evidence from image/scene

#### **FR-4 Repair vs Replace Decision**

* System SHALL recommend either:

  * `repair` or `replace`
* System SHALL include a rationale

#### **FR-5 Repair Plan Generation**

If repair is recommended:

* System SHALL return:

  * difficulty level (1–5)
  * estimated time
  * list of tools
  * list of parts
  * step-by-step instructions

#### **FR-6 Structured Output**

* Output MUST be valid JSON
* JSON schema must be stable for downstream phases

---

### **Non-Functional Requirements**

* Response time < 10 seconds
* Deterministic parsing (no free text)
* All results persistable to disk

---

### **Acceptance Criteria**

✅ Upload image → receive structured diagnosis
✅ Output is machine-readable JSON
✅ No human interpretation needed to read results

---

### **Deliverables**

* FastAPI endpoint
* YOLO (or stub) perception module
* LLM reasoning prompt
* JSON schema definition
* Sample test images + outputs

---

---

# **BRD – Phase 2**

## **FixBrain v0.2: Confidence, Gaps & Follow-Up Intelligence**

### **Objective**

Enable FixBrain to recognize **uncertainty** and request **additional information**.

This is where it starts behaving like an **agent**, not a static analyzer.

---

### **In Scope**

* Confidence scoring
* Missing-information detection
* Follow-up requests (questions or images)

---

### **Out of Scope**

* Automated tool execution
* Parts sourcing
* User tool matching

---

### **New Functional Requirements**

#### **FR-7 Confidence Assessment**

* System SHALL output an overall confidence score (0–1)

#### **FR-8 Information Gap Detection**

* System SHALL identify:

  * missing views (e.g., underside, label)
  * missing metadata (brand/model)

#### **FR-9 Follow-Up Requests**

* System SHALL return a list of required next inputs:

  * “take photo of pump label”
  * “confirm appliance age”

Example:

```json
"needs_more_info": [
  {
    "type": "image",
    "description": "Photo of drain pump label"
  }
]
```

---

### **Acceptance Criteria**

✅ System asks for more info when uncertain
✅ System does NOT hallucinate confidence

---

---

# **BRD – Phase 3**

## **FixBrain v0.3: Tool Inventory Intelligence**

### **Objective**

Optimize repair plans based on **tools the user actually owns**.

This is a **major differentiation**.

---

### **In Scope**

* Tool inventory storage
* Tool capability reasoning
* Repair plan adaptation

---

### **Out of Scope**

* Purchasing tools
* Autonomous robot usage

---

### **Functional Requirements**

#### **FR-10 Tool Inventory**

* System SHALL store user tools:

  * tool name
  * size/spec
  * capability tags

#### **FR-11 Tool Compatibility Check**

* System SHALL validate each repair step against available tools

#### **FR-12 Plan Optimization**

* If required tool is missing:

  * suggest alternative steps
  * OR recommend replacement
  * OR suggest tool acquisition

Example output:

```json
"tool_compatibility": {
  "missing_tools": ["Torx T20"],
  "workarounds_available": false
}
```

---

### **Acceptance Criteria**

✅ Repair plan changes based on tools
✅ Clear explanation when repair is blocked

---

---

# **BRD – Phase 4**

## **FixBrain v0.4: Parts Intelligence & Sourcing**

### **Objective**

Automatically identify and source **exact or compatible parts**.

---

### **In Scope**

* Part identification
* OEM vs aftermarket comparison
* Cost/time estimation

---

### **Out of Scope**

* Payment processing
* Inventory guarantees

---

### **Functional Requirements**

#### **FR-13 Part Identification**

* System SHALL map generic parts → OEM part numbers

#### **FR-14 Vendor Search**

* System SHALL query multiple vendors
* Return price, delivery time, reliability score

#### **FR-15 Cost Optimization**

* System SHALL compute:

  * repair cost
  * replacement cost
  * break-even point

---

### **Acceptance Criteria**

✅ Exact part numbers identified
✅ Clear cost-based recommendation

---

---

# **BRD – Phase 5**

## **FixBrain v1.0: Full Agentic Repair Orchestration**

### **Objective**

Enable **multi-step agentic behavior** with tool execution loops.

---

### **In Scope**

* Tool calling
* Multi-step reasoning
* Iterative perception
* Safety validation

---

### **Functional Requirements**

#### **FR-16 Agent Loop**

* System SHALL:

  * reason
  * call tools
  * observe results
  * re-plan

#### **FR-17 Tool Governance**

* Only approved tools may be invoked
* Hard safety rules enforced

#### **FR-18 Final Execution Plan**

* Output fully validated, optimized repair workflow

---

### **Acceptance Criteria**

✅ Multi-step reasoning demonstrated
✅ Tool calls logged and traceable

---

# 🎯 How to Use This with Codex

1. Give **Phase 1 BRD only**
2. Ask Codex:

   > “Implement FixBrain Phase 1 strictly per BRD”
3. Test Phase 1 thoroughly
4. Move to Phase 2 without refactor

---

## One-line framing you can use with YC or engineers:

> “We are building FixBrain in tightly scoped phases, starting with deterministic visual diagnosis and expanding into a fully agentic repair intelligence platform.”

If you want next, I can:

* Convert Phase 1 BRD into **engineering tickets**
* Create a **Notion-ready BRD table**
* Generate **Phase 1 test cases & failure modes**

Just tell me.
