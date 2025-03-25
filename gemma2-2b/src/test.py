import requests
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("endpoint", help="the url endpoint, such as http://localhost:8000")
args = parser.parse_args()

url = args.endpoint

# Data to be sent

USER_PROMPT = 'tell me about wwii'

print (f'USER PROMPT: {USER_PROMPT}')

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
