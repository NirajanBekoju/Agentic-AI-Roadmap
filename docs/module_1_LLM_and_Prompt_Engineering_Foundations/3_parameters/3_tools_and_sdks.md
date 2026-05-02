# Tools & SDKs
The essential Python ecosystem for building production LLM applications.

* **OpenAI SDK:** Official Python client for GPT-4o and o-series models. Also works with any OpenAI-compatible endpoint (Ollama, vLLM, Groq).
* **Anthropic SDK:** Official client for Claude models. Includes streaming, tool use, vision, and document handling. Async support via `AsyncAnthropic`.
* **Pydantic v2:** Type validation and serialization. Define data shapes; Pydantic validates LLM outputs against them and provides clear error messages for retries.
* **Instructor:** Wraps any LLM SDK with automatic Pydantic validation and retry logic. Converts structured output from "hard" to "trivial."
* **LangChain / LlamaIndex:** Higher-level frameworks for chains, agents, RAG pipelines. Useful for prototyping; prefer direct SDK calls in production for control.
* **vLLM:** High-throughput inference server for open-source models. PagedAttention enables 20–30× higher throughput than naive batching.

## Starter installation

```bash
pip install anthropic openai pydantic instructor tiktoken python-dotenv
```

## Complete working example — fault classification pipeline
End-to-end: fault log → structured diagnosis

```python
import os
from pydantic import BaseModel, Field
from typing import Literal
import instructor
import anthropic

class FaultReport(BaseModel):
    fault_codes: list[str] = Field(description="OBD-II codes found")
    bucket: Literal["Cylinder Issues", "Turbo", "Bad Sensor", "Unknown"]
    root_cause: str = Field(description="Most likely root cause in one sentence")
    confidence: float = Field(ge=0.0, le=1.0)
    action: str = Field(description="Recommended next action")
    reasoning: str = Field(description="Step-by-step diagnostic reasoning")

client = instructor.from_anthropic(anthropic.Anthropic())

SYSTEM = """You are an expert diesel engine fault analyst. Analyze fault logs step by step. 
Always explain your reasoning before classifying. Use OBD-II knowledge and cross-reference symptoms."""

def diagnose(fault_log: str) -> FaultReport:
    return client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": fault_log}],
        response_model=FaultReport,
    )

# Example usage
report = diagnose("""
P0303: Cylinder 3 misfire (count: 142 in last 10min)
Exhaust temp sensor 3: +47°C above baseline
Fuel trim bank 1: +9.2% (long term)
Engine hours: 8,423
Last service: 7,900h (spark plugs replaced)
""")

print(f"Bucket: {report.bucket}")
print(f"Confidence: {report.confidence:.0%}")
print(f"Root cause: {report.root_cause}")
print(f"Action: {report.action}")
```

## Next steps
Now that you have the foundations: explore agentic patterns (tool use, multi-agent), RAG for knowledge augmentation, and evals for measuring prompt quality systematically. The real leverage is in measuring your prompts, not just writing them.