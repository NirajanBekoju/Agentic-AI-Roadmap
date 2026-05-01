## Transformer Architecture

*The self-attention mechanism that powers every major LLM — from GPT-4 to Llama 3 to Claude.*

All modern LLMs are built on the Transformer architecture (Vaswani et al., 2017). The key innovation is self-attention: every token can attend to every other token in the context window simultaneously, capturing long-range dependencies that RNNs struggled with.

---

### Core Components

* **Token embedding:** Token IDs → dense vectors in high-dimensional space. Similar meanings cluster together. Dimensionality: 4096–8192 for large models.
* **Positional encoding:** Since attention is order-agnostic, position information is injected. Modern models use RoPE (Rotary Position Embedding) for length extrapolation.
* **Multi-head attention:** Each head learns different relationship types (syntax, coreference, semantics). Heads run in parallel and concatenate their outputs.
* **Feed-forward network:** After attention, each position passes through a 2-layer MLP independently. This is where most "knowledge" is stored in the weights.

---
### Attention in One Equation

**Scaled dot-product attention**

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

* **Q** = Query matrix (what am I looking for?)
* **K** = Key matrix (what do I contain?)
* **V** = Value matrix (what do I output?)
* **d_k** = Key dimension (scaling prevents vanishing gradients)