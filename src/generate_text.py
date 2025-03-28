import requests
import sys
import argparse
import json
import apicalls

parser = argparse.ArgumentParser()
parser.add_argument("--model", help="model id, such as gemma3-1b")
parser.add_argument("--endpoint", help="the url endpoint, such as http://localhost:8000")
args = parser.parse_args()

url = args.endpoint
modelstr = args.model

headers = { "Content-Type": "application/json", 'Host': 'llm-service' }

model = apicalls.get_model(modelstr)

user_prompt = 'tell me about wwii'

data = model.build_request_data(user_prompt, 128)
path = model.get_genai_path()

print ('REQUEST HEADER', headers)
print ('REQUEST DATA  ', json.dumps(data))

response = requests.post(f'{url}/{path}', 
                        data=json.dumps(data), 
                        headers=headers, timeout=1000)

# Print the response
print('RESPONSE RESULT ', response.reason)
print('RESPONSE_CODE   ', response.status_code)
print('RESPONSE CONTENT', response.content.decode())
