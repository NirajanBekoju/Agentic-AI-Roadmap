## LLM Types & Taxonomy

*Not all LLMs are equal — understanding the taxonomy helps you choose the right model for the job.*

---

### By Training Stage

* **Base model**
* **Instruct / Chat**
* **RLHF / RLAIF**
* **Fine-tuned**

**Base Model**
Trained purely on next-token prediction. Excellent at completion tasks, but will "complete" rather than follow instructions. Example: `Llama-3-70b` (base). Useful for fine-tuning, less useful for direct chat.

> Base models complete any pattern — give them a story opening and they continue it; give them half a Python function and they finish it. They have no concept of "roles" or "helpfulness."

**Focus: Instruct / Chat Model**
Trained via Supervised Fine-Tuning (SFT) on massive datasets of question-and-answer pairs or structured instructions. These models are explicitly taught to act as helpful assistants rather than just text predictors. Example: `Meta-Llama-3-70B-Instruct`. Ideal for general user interaction, chatbots, and zero-shot prompting.

> Instruct models shift the paradigm from "complete the text" to "answer the prompt." If you give them a question, they will attempt to provide the answer, whereas a base model might just generate a list of similar questions.

**RLHF / RLAIF Model**
These models have undergone an alignment phase using Reinforcement Learning from Human Feedback (RLHF) or AI Feedback (RLAIF). A separate "reward model" scores the LLM's responses based on human preferences (typically maximizing helpfulness, harmlessness, and honesty), and the LLM updates its weights to favor high-scoring behaviors. 

> Alignment is what turns a highly capable but unpredictable text generator into a safe, conversational agent. It smooths out the rough edges, significantly reducing toxic outputs and teaching the model when it is appropriate to refuse an unsafe request.

**Fine-Tuned Model**
A model (usually starting from a Base or Instruct model) that has been further trained on a highly specialized, domain-specific dataset. This can be done via full-parameter fine-tuning or parameter-efficient methods like LoRA/QLoRA. Example: A generic base model fine-tuned entirely on a company's internal codebase or medical literature (`Med-PaLM`).

> Fine-tuning is less about teaching the model entirely new knowledge and more about teaching it a specific *behavior*, *format*, or *tone*. It transforms a generalist into a domain expert, making it highly reliable for niche, repetitive tasks where prompt engineering isn't enough.

---

### By Access Model

| Dimension | Proprietary API | Open-source |
| :--- | :--- | :--- |
| **Examples** | GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 | Llama 3 (8B/70B), Mistral, Qwen 2.5 |
| **Access** | REST API, pay-per-token | Download weights, self-host |
| **Privacy** | Data leaves your infra | Fully on-prem possible |
| **Quality ceiling** | State of the art | Approaching SOTA at 70B+ |
| **Cost at scale** | Linear with usage | Fixed infra + GPU cost |
| **Customization** | Limited (fine-tuning API) | Full weight access, any technique |