import requests
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("endpoint", help="the url endpoint, such as http://localhost:8000")
args = parser.parse_args()

url = args.endpoint

response = requests.get(f'{url}/metrics', headers={"Host": "35.202.125.152"})

# Print the response
print(response.content.decode())
