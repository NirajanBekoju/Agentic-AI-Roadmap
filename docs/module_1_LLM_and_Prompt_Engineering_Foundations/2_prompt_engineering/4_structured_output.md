# Structured Output & JSON Parsing

**Reliably extracting machine-readable data from LLM responses — the bridge between language models and software systems.**

LLMs produce text. Your application needs data. **Structured output** is the discipline of reliably converting LLM responses into typed, validated data structures your code can use.

---

### Approaches Ranked by Reliability

1. **Native JSON Mode**
2. **Instructor / Pydantic**
3. **Manual Parsing**

---

### 1. Native JSON Mode
Most frontier APIs now support a `response_format` parameter that forces JSON output. The model is constrained at the decoding level to only emit valid JSON tokens.

#### OpenAI JSON Mode Example (Python)

```python
from openai import OpenAI
import json

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system", 
            "content": "Extract fault data as JSON with fields: fault_code, severity, component, action_required"
        },
        {
            "role": "user", 
            "content": "P0303 cylinder 3 misfire detected during cold start"
        }
    ]
)

# Parsing the string response into a dictionary
data = json.loads(response.choices[0].message.content)

# Resulting Object:
# {
#   "fault_code": "P0303", 
#   "severity": "medium", 
#   "component": "cylinder_3_ignition", 
#   "action_required": true
# }
```

### 2. Instructor & Pydantic Validation

**Instructor** wraps the API with Pydantic validation. If the model returns invalid JSON or a schema mismatch, it can automatically retry by providing the validation error back to the model as feedback.

#### Instructor + Pydantic Example (Python)

```python
import instructor
import anthropic
from pydantic import BaseModel, Field
from typing import Literal

# Define your data structure
class FaultDiagnosis(BaseModel):
    fault_code: str = Field(description="OBD-II fault code")
    component: str = Field(description="Affected engine component")
    severity: Literal["low", "medium", "high", "critical"]
    confidence: float = Field(ge=0.0, le=1.0)
    recommended_action: str

# Patch the Anthropic client with Instructor
client = instructor.from_anthropic(anthropic.Anthropic())

diagnosis = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "P0303 misfire, high exhaust temp"}
    ],
    response_model=FaultDiagnosis,
)

print(diagnosis.severity)    # Output: "high"
print(diagnosis.confidence)  # Output: 0.87

```
## Key Strategy: Schema in the Prompt

Always include your exact **JSON schema** in the system prompt with field descriptions. Models produce dramatically better structured output when shown exactly what to fill in versus being asked to simply "return JSON."

---

### Why this works
By defining a `BaseModel`, you provide the LLM with a strict template. Tools like **Instructor** then use this schema to generate a system prompt that guides the model's internal reasoning toward the desired output format.

> **Pro Tip:** When you provide a schema, you aren't just asking for JSON; you are providing the model with a **semantic map**. The field names and descriptions act as additional context that helps the model understand exactly which parts of the input text belong in which field.

### 3. Manual Parsing

When you can't use native JSON mode or libraries like **Instructor**, use regex extraction with multiple fallbacks. Defensive parsing is critical to handle model unpredictability.


```python
import re, json

def extract_json(text: str) -> dict | None:
    # Try 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try 2: extract from code fence
    fence = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try 3: find first {...} block
    brace = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if brace:
        try:
            return json.loads(brace.group())
        except json.JSONDecodeError:
            pass
    
    return None  # signal upstream to retry
```

### Schema in the Prompt

Always include your exact **JSON schema** in the system prompt with field descriptions. Models produce dramatically better structured output when shown exactly what to fill in versus simply being asked to "return JSON."