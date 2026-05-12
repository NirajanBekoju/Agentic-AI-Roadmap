import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hello, how many tokens am I using?"
tokens = enc.encode(text)

print(f"{len(tokens)} tokens: {tokens}")
