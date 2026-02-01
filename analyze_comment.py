import os
import requests
import json

def run_analysis():
    # Use 127.0.0.1 to avoid Windows "localhost" resolution delays
    url = "http://127.0.0.1:11434/api/generate"
    comment = os.getenv("COMMENT_BODY", "Analyze this code.")

    payload = {
        "model": "deepseek-r1:7b",
        "prompt": f"Research this PR comment: {comment}",
        "stream": False
    }

    print(f"--- Sending request to Ollama at {url} ---")
    
    try:
        # We add a longer timeout (300s) because your logs show '0B VRAM' (CPU mode is slow)
        response = requests.post(url, json=payload, timeout=300)
        
        print(f"Ollama Response Code: {response.status_code}")
        ai_response = response.json().get('response', 'No response text.')

        with open("research_report.md", "w", encoding="utf-8") as f:
            f.write(f"### 🛡️ DeepSeek Analysis\n\n{ai_response}")
            
    except Exception as e:
        error_msg = f"Runner failed to hit Ollama. Error: {str(e)}"
        print(error_msg)
        with open("research_report.md", "w") as f:
            f.write(error_msg)

if __name__ == "__main__":
    run_analysis()