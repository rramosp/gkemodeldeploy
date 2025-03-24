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
    "model": "google/gemma-3-4b-it",
    "messages": [
        {
          "role": "user",
          "content": USER_PROMPT
        }
    ],
    "max_tokens": 128

}


# A POST request to the API
response = requests.post(f'{url}/v1/chat/completions', json=data)

# Print the response
print(response.json())
