# Temperature & Sampling Parameters

Control the randomness of generation — the difference between deterministic analysis and creative exploration.

After the model computes logits (raw scores) for each possible next token, **sampling parameters** control how a token is selected from that distribution. This is where you trade off creativity for consistency.

---

## Sampling Parameters Reference

| Parameter | Range | Effect | Use Case |
| :--- | :--- | :--- | :--- |
| **temperature** | 0–2 | Scales logit distribution. Low = peaked (deterministic), high = flat (random) | 0 for extraction; 0.7 for chat; 1.0+ for creative |
| **top_p** | 0–1 | **Nucleus sampling** — only sample from top tokens summing to p% probability mass | 0.9 is a safe default. Use instead of or alongside temp |
| **top_k** | 1–∞ | Limit to top-k highest probability tokens | 50 is common. Harder cutoff than top_p |
| **max_tokens** | 1–context | Maximum tokens to generate | Set to 2× your expected output length |
| **stop sequences** | list | Generation halts when any sequence is produced | Use with structured formats: `["</answer>", "```"]` |

---

> ### ⚠️ Common Mistake
> Setting `temperature=0` doesn't guarantee 100% reproducibility. Floating-point non-determinism and batching means you may get slightly different results. For true determinism, use a **seed** parameter and fix your infrastructure.

---

## Recommended Settings by Task Type

```python
CONFIGS = { 
    "extraction": {"temperature": 0.0, "top_p": 1.0}, 
    "analysis":   {"temperature": 0.2, "top_p": 0.9}, 
    "chat":       {"temperature": 0.7, "top_p": 0.9}, 
    "creative":   {"temperature": 1.0, "top_p": 0.95}, 
    "brainstorm": {"temperature": 1.3, "top_p": 0.98}, 
}
```