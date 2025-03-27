import time
import numpy as np
from locust import HttpUser, task, between
import os
import subprocess
from loguru import logger

questions = [
    "What's the capital of France?",
    "Summarize the plot of Hamlet.",
    "Explain photosynthesis in one sentence.",
    "Write a short poem about autumn.",
    "Convert 10 degrees Celsius to Fahrenheit.",
    "What are the prime numbers between 10 and 20?",
    "Define 'quantum entanglement.'",
    "Give me three synonyms for 'happy'.",
    "What is the chemical symbol for gold?",
    "Who painted the Mona Lisa?"
]

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class LLMUser(HttpUser):
    wait_time = between(0,1)

    @task
    def generate_content(self):

        hostname = os.getenv('HOSTNAME')
        hostname = subprocess.run(['hostname', '-I'], capture_output=True).stdout.decode().strip()
    
        question = questions[np.random.randint(len(questions))]
        num_tokens = np.random.randint(1000) + 128

        url = "/generate"  
        data = {
                "inputs": f"<start_of_turn>user\n{question}<end_of_turn>\n",
                "parameters": {
                                "temperature": 0.90,
                                "top_p": 0.95,
                                "max_new_tokens": num_tokens
                            }
                }
        headers = {"Content-Type": "application/json"} # example header.

        r = self.client.post(url, json=data, headers=headers, name="Post Resource") # send Json data.
        logger.info (f"{hostname} -- num_tokens={num_tokens:6d}, r.status_code={r.status_code:4d}, r.reason={r.reason}")