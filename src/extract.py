import requests
import json 
import sys 

# Global configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

def extract_entities(text):
    # Define the strict schema
    schema = {
        "people": ["list of names"], 
        "dates": ["list of dates"], 
        "locations": ["list of locations"]
    }

    prompt = f"""
    Extract names of people, dates, and locations from the following text.
    Return the result strictly as a JSON object following this format: {json.dumps(schema)}
    Do not include any preamble, explanations, or markdown formatting. 
    Only return valid JSON.

    TEXT:
    {text}
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt, 
        "stream": False, 
        "format": "json"
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result["response"]

    except requests.exceptions.Timeout:
        return "Error: Request timed out. Ollama server may be slow or unresponsive."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract.py 'your messy text here'")
    else:
        input_text = sys.argv[1]
        structured_data = extract_entities(input_text)
        print(structured_data)