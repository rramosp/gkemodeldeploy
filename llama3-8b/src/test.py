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
        "model": "meta-llama/Meta-Llama-3-8B",
        "prompt": USER_PROMPT, 
        "use_beam_search": False, 
        "max_tokens": 128,
        "temperature":1.0
}
  
response = requests.post(f'{url}/v1/completions', json=data)

# Print the response
print(response.json())
