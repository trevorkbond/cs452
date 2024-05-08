import json
import requests

# Load API key from a config.json
with open("config.json") as config:
    apikey = json.load(config)["apikey"]

# method to call chat gpt through web request (portable to any language)
# see https://platform.openai.com/docs/models/overview for different models
def call_chatgpt(prompt, model="gpt-3.5-turbo", api_key="your_api_key_here"):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            #{"role": "system", "content": "TBD"},
            {"role": "user", "content": prompt}
        ]
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
