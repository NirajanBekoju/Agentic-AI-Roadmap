# Models & API Overview

The landscape of production-ready models available today — proprietary and open-source.

---

## Proprietary Frontier Models

| Model | Provider | Context | Key Strengths |
| :--- | :--- | :--- | :--- |
| **GPT-4o** | OpenAI | 128K | Vision, function calling, broad capability |
| **Claude Sonnet 4.5** | Anthropic | 200K | Long context, reasoning, code, instruction following |
| **Gemini 1.5 Pro** | Google | 1M+ | Massive context window, native video understanding |

### Best For:
* **GPT-4o:** Production apps, multimodal pipelines.
* **Claude Sonnet 4.5:** Document analysis, agentic tasks, safety-critical applications.
* **Gemini 1.5 Pro:** Full codebase analysis, long video QA.

---

## Open-source Models via Ollama / vLLM

* **Llama 3 8B** (Meta): Ideal for self-hosting on consumer hardware.
* **Llama 3 70B** (Meta): High performance requiring a GPU cluster.
* **Mistral 7B** (Mistral AI): Highly efficient for its size.

---

### Spin up Llama 3 locally with Ollama

```bash
# Install Ollama 
curl -fsSL [https://ollama.ai/install.sh](https://ollama.ai/install.sh) | sh 

# Pull and run Llama 3 8B 
ollama pull llama3:8b 
ollama run llama3:8b 

# Or use the OpenAI-compatible API 
ollama serve # starts on http://localhost:11434
```

### Use Ollama with OpenAI-compatible SDK

```python
from openai import OpenAI 

# Point to local Ollama server 
client = OpenAI(
    base_url="http://localhost:11434/v1", 
    api_key="ollama"
) 

response = client.chat.completions.create( 
    model="llama3:8b", 
    messages=[{
        "role": "user", 
        "content": "Explain attention in one paragraph."
    }] 
) 

print(response.choices[0].message.content)
```