import requests
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("endpoint", help="the url endpoint, such as http://localhost:8000")
args = parser.parse_args()

url = args.endpoint

response = requests.get(f'{url}', headers={"Host": "34.67.199.151"})

# Print the response
print(response.content.decode())
