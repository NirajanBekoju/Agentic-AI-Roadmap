# Roles & Message Structure

The conversation format is the API primitive you'll use for everything. Understanding roles is foundational. 

Modern LLM APIs use a `messages` array where each message has a role and content. The model is trained to respond differently based on role — this is not a UX convention, it's baked into the weights.

### Example Interaction

**System**
> You are an expert Python engineer. Always include type hints and docstrings. Return only code — no explanations unless asked. If a request is ambiguous, ask one clarifying question.

**User**
> Write a function that validates an email address.

**Assistant**
```python
import re

def validate_email(email: str) -> bool:
    """Validate an email address using RFC 5322 pattern."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Role Semantics

| Role | Purpose | Persists across turns? |
| :--- | :--- | :--- |
| **system** | Sets persona, constraints, format, context. The model treats this as ground truth about its environment. | Yes — sent every request |
| **user** | The human's turn. Questions, tasks, feedback, uploaded content. | No — per-turn |
| **assistant** | Prior model outputs included in multi-turn history. You can also pre-fill this to steer the response. | Accumulates in history |


## System Prompt Design Patterns

**Minimal production system prompt structure:**

```text
# Role
You are [persona] specializing in [domain].

# Constraints  
- [Hard rule 1]
- [Hard rule 2]

# Output format
Respond in JSON matching this schema:
{"field": "type", ...}

# Context
[Any static context the model needs every turn]
```

> **Pro tip:** 
> You can prefill the `assistant` role to force output format. Start with `{"` and the model will continue generating a JSON object — no preamble, no markdown fences.

---

## Multi-Turn Conversation Structure

**Maintaining conversation history:**
```python
import anthropic

client = anthropic.Anthropic()
history = []

def chat(user_msg: str) -> str:
    history.append({"role": "user", "content": user_msg})
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="You are a helpful AI assistant.",
        messages=history
    )
    
    assistant_msg = response.content[0].text
    history.append({"role": "assistant", "content": assistant_msg})
    return assistant_msg
```