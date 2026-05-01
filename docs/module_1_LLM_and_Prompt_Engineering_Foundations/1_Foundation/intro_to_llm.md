## Chapter 1: What is a Large Language Model?

*A deep dive into the statistical engines reshaping how software is built — from transformer weights to deployment APIs.*

A **Large Language Model (LLM)** is a deep neural network trained on massive corpora of text to predict the probability of the next token given all prior tokens. Despite this deceptively simple objective, emergent capabilities — reasoning, instruction following, code generation — appear at sufficient scale.

---

### Core Mechanics

* 📊 **Scale:** Billions to trillions of parameters learned from hundreds of billions of tokens across the web, books, and code.
* 🎯 **Training objective:** Next-token prediction via cross-entropy loss. The model learns to compress all of human text into a prediction function.
* ⚡ **Inference:** Autoregressive: one token sampled at a time from the predicted distribution, appended, and fed back in.
* 🔧 **Alignment:** RLHF & Constitutional AI fine-tune base models to follow instructions, refuse harmful requests, and be helpful.

---

### How Training Works

Pretraining processes text in chunks called **context windows**. For each position in the window, the model predicts the next token. Gradients are backpropagated through all layers to minimize prediction error. After billions of gradient steps, the weights encode a compressed representation of language structure, facts, and reasoning patterns.

> **Key Insight:** LLMs don't retrieve stored answers — they *generate* continuations. Every response is a fresh sample from a learned probability distribution conditioned on your input.

---

### The Emergent Capabilities Threshold

Below ~7B parameters, models can complete text and follow simple patterns. Above ~70B, qualitatively new abilities emerge: multi-step reasoning, analogical thinking, and in-context learning — adapting to new tasks from examples alone, with no weight updates.

**Key Emergent Capabilities:**
* In-context learning
* Chain-of-thought reasoning
* Code generation
* Tool use
* Instruction following
* Multilingual transfer