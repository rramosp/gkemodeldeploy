import requests
import sys

if len(sys.argv)!=2:
   print('must include one arg with the API endpoint')
   exit(-1)

url = sys.argv[1]

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
