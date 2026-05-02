# Core Prompting Techniques
The prompt engineering toolkit — from zero-shot to few-shot to structured elicitation.

## Key Techniques
* **Zero-shot:** Instructions only.
* **Few-shot:** Providing a few examples of input-output pairs to guide the model.
* **Negative examples:** Showing the model what *not* to do.
* **Role prompting:** Assigning a specific persona to the model (e.g., "Act as a senior software engineer").

---
### 1. Zero-Shot Prompting
**Zero-shot prompting** gives the model only instructions with no examples. It works well for well-defined tasks when using frontier models.

### Example Prompt
> Classify the sentiment of this review as POSITIVE, NEGATIVE, or NEUTRAL.
>
> **Review:** "The food was okay but the service was incredibly slow."
>
> **Sentiment:**

* **Best for:** Clear tasks, frontier models, and situations where you have no labeled examples.
* **Limitations:** Falls short for specialized formats or nuanced categorization.

---
### 2. Few-Shot Prompting
**Few-shot prompting** prepends 2–8 input → output examples before the real query. This allows the model to pattern-match the specific format, tone, and logic required.

### Example Prompt
> Extract structured data from the review.
>
> **Review:** "Amazing pasta, great staff, tiny portions."
> **Output:** {"sentiment":"positive","aspects":["food:positive","staff:positive","portion:negative"]}
>
> **Review:** "Overpriced and cold food."
> **Output:** {"sentiment":"negative","aspects":["price:negative","food:negative"]}
>
> **Review:** "Decent cocktails, loud music, friendly bartender."
> **Output:** ---

### Strategy & Usage
* **Best for:** Enforcing strict output formats (like JSON), teaching nuanced classification, and ensuring consistent structured output.
* **Pro Tip:** Use **3–5 diverse examples** to cover different edge cases and prevent the model from becoming biased toward one specific type of answer.

---

### 3. Negative Examples
**Negative examples** explicitly show the model what **NOT** to do. This technique is highly effective for grounding the model and dramatically reducing unwanted behaviors or repetitive conversational filler.

### Example Prompt
> ### # What NOT to do:
> * ❌ "I'd be happy to help! Here's a summary of..."
> * ❌ Adding markdown headers when plain text is requested
> * ❌ Ending with "Let me know if you need anything else!"
>
> ### # Do this instead:
> * ✓ Begin directly with the content requested
> * ✓ Match the exact format specified
> * ✓ Stop when the task is complete

---

### Why it works
* **Eliminates Sycophancy:** Stops the model from using overly polite preambles or "AI-isms."
* **Fixes Format Drift:** Prevents the model from accidentally adding stylistic elements (like bolding or headers) that break downstream parsers.
* **Enforces Brevity:** Ensures the output is concise and focused solely on the task at hand.

---
### 4. Role Prompting
**Role prompting** assigns an expert identity to the model. This technique activates relevant knowledge clusters and shifts the output's tone, depth, and vocabulary to match a specific professional standard.

#### Example Prompt
> **Role:** You are a senior site reliability engineer (SRE) at a high-traffic fintech. 
> **Methodology:** You approach problems by first identifying blast radius, then root cause. 
> **Communication Style:** You communicate in precise technical terms and skip preamble.
>
> **User:** Our $p99$ latency jumped from 80ms to 2.1s at 14:32 UTC. What's your diagnostic approach?

---

#### Why Specificity Matters
* **Avoid Generic Roles:** A prompt like "expert engineer" is weak and results in broad answers.
* **Define the Persona:** Using "Senior SRE at a high-traffic fintech who skips preamble" is strong. 
* **Knowledge Activation:** The more contextual detail you provide, the more precisely the model activates the specific technical knowledge and cultural norms associated with that role.

## Prompt Engineering Best Practices

### 🎯 Be Specific, Not Polite
"Please could you possibly..." wastes tokens and adds ambiguity. **State the task directly.**

### 🚫 Specify What You Don't Want
Negative constraints are often more efficient than trying to describe the positive space exhaustively.

### 🏷️ Use XML Tags for Structure
Help models parse complex prompts reliably by using tags like:
* `<context>`
* `<task>`
* `<examples>`

### 🔚 Put Instructions at the End
For long contexts, models attend more strongly to recent tokens. **Place the most important instructions last.**

### 🧪 Iterate Empirically
Treat prompts like code:
1.  **Version** them.
2.  **Test** against a fixed evaluation set.
3.  **Measure** changes in performance.