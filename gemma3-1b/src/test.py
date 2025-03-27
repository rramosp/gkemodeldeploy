import requests
import sys
import argparse
import json

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

headers = { 'Host': '35.202.125.152',
    "Content-Type": "application/json",
}
print (json.dumps(data))

# A POST request to the API
response = requests.post(f'{url}/v1/chat/completions', 
                        data=json.dumps(data), 
                        headers=headers, timeout=1000)

# Print the response
print(dir(response))
print(response.reason)
print(response.status_code)
print(response.content.decode())
