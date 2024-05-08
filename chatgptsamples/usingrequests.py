import json
import requests
with open("config.json") as config:
    apikey = json.load(config)["apikey"]

def call_chatgpt(prompt, model="gpt-3.5-turbo", api_key="your_api_key_here"):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Example usage:
prompt = "Tell me about the benefits of meditation."
result = call_chatgpt(prompt, api_key=apikey)

print(result)
