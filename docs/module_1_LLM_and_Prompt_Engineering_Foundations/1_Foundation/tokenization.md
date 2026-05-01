## Tokenization

*LLMs don't read characters or words — they read tokens. Understanding tokenization explains many model quirks.*

A **tokenizer** converts raw text into a sequence of integers (token IDs). The vocabulary is built using Byte-Pair Encoding (BPE) or similar algorithms — frequent subword sequences become single tokens, rare ones split into smaller pieces.

---

### Token Visualizer

The boundaries below indicate how text is split into tokens. Common words become single tokens; rare or technical terms split into multiple.

`The` | `quick` | `brown` | `fox` | `un` | `expect` | `edly` | `ran` | `through` | `the` | `JSON` | `ify` | `();`

**Legend:**
- 🟣 High-frequency tokens  
- 🟢 Medium-frequency tokens  
- ⚪ Low-frequency / split tokens  

---

### Why Tokens Matter for Prompting

- 💰 **Pricing:** APIs charge per token (input + output). A 1000-word document ≈ 1300–1500 tokens.
- 📏 **Context limits:**  
  - Claude 3.5 Sonnet: 200K tokens  
  - GPT-4o: 128K tokens  
  - Llama 3 70B: 8K–128K tokens
- 🧮 **Counting quirks:** Spaces, punctuation, and capitalization all affect tokenization. `GPT-4o` may be 3 tokens; `gpt4o` may be 2.
- 🌍 **Non-English text:** Often tokenizes less efficiently, requiring more tokens for the same meaning compared to English.

---

### Token Counting with `tiktoken`

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hello, how many tokens am I using?"
tokens = enc.encode(text)

print(f"{len(tokens)} tokens: {tokens}")
# Output: 9 tokens: [9906, 11, 1268, 1690, 11460, 939, 358, 1701, 30]
```
