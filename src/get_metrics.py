import requests
import sys
import argparse
import apicalls

parser = argparse.ArgumentParser()
parser.add_argument("--model", help="model id, such as gemma3-1b")
parser.add_argument("--endpoint", help="the url endpoint, such as http://localhost:8000")
args = parser.parse_args()

url = args.endpoint
modelstr = args.model

headers = { "Content-Type": "application/json", 'Host': 'llm-service' }

model = apicalls.get_model(modelstr)

path = model.get_metrics_path()

response = requests.get(f'{url}/{path}', headers=headers)

# Print the response
print(response.content.decode())
