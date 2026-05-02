## Chain of Thought (CoT) Reasoning
**Chain of Thought (CoT)** prompting asks the model to produce intermediate reasoning steps before the final answer. This dramatically improves performance on math, logic, multi-step planning, and diagnostic tasks.

### Why it Works
Transformers allocate a fixed amount of "compute" per generated token. Complex reasoning compressed into a single token often fails. By generating intermediate steps, the model effectively "thinks" across more tokens, using later steps to condition on and correct earlier logic.

---

### CoT Implementation Strategies

| Strategy | Description |
| :--- | :--- |
| **Zero-shot CoT** | Simply add "Let's think step by step" or "Think through this carefully." |
| **Few-shot CoT** | Provide examples that include reasoning chains to teach a specific logic style. |
| **Scratchpad / Tags** | Use `<think>` or `<reasoning>` tags to separate the logic from the final output. |
| **Self-consistency** | Run the prompt multiple times and use a majority vote for the final answer. |

---

### CoT in Practice: Scratchpad Pattern
**Prompt:**
> You will analyze this engine fault log. Before giving your diagnosis, reason through each symptom systematically.
>
> <fault_log>
> Cylinder 3 misfire P0303. Exhaust temp sensor +45°C above baseline.
> Fuel trim: +8.5%. Spark plugs last replaced 95k km ago.
> </fault_log>
>
> Think through the possible root causes step by step inside `<reasoning>` tags, then give your final diagnosis in `<diagnosis>` tags.

**Response:**
> <reasoning>
> 1. **P0303** = Cylinder 3 misfire. Primary suspects: spark plug, ignition coil, fuel injector.
> 2. **Spark plugs at 95k km** — manufacturer interval typically 80-100k. Likely degraded.
> 3. **Elevated exhaust temp:** Misfires send unburnt fuel to exhaust, oxidizing there → temp spike.
> 4. **+8.5% positive fuel trim:** ECU adding fuel to compensate for lean condition.
> 5. **Conclusion:** Worn spark plug on Cylinder 3 causing intermittent misfire.
> </reasoning>
>
> <diagnosis>
> **Primary:** Cylinder 3 spark plug failure.
> **Action:** Replace all spark plugs, clear P0303, road test.
> </diagnosis>

---

### ⚠️ Limitation
CoT increases the number of output tokens, which raises **cost and latency**. 
* **Use for:** High-stakes decisions or complex logic where accuracy is paramount.
* **Skip for:** High-volume, low-complexity tasks where speed and economy are priorities.