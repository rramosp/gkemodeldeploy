import requests

# The API endpoint
url = "http://localhost:8000"
#url = "http://localhost:9000"
#url = "http://34.59.102.106:8000"

# Data to be sent

USER_PROMPT = 'tell me about wwii'

data = {
    "inputs": f"<start_of_turn>user\n{USER_PROMPT}<end_of_turn>\n",
    "parameters": {
        "temperature": 0.90,
        "top_p": 0.95,
        "max_new_tokens": 128
    }
}

# A POST request to the API
response = requests.post(url, json=data)

# Print the response
print(response.json())
