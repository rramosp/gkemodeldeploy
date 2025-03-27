import time
import numpy as np
from locust import HttpUser, task, between
import os
import subprocess
from loguru import logger
import json
import requests

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

class LLMUser(HttpUser):
    wait_time = between(0,1)

    @task
    def generate_content(self):

        question = questions[np.random.randint(len(questions))]
        num_tokens = np.random.randint(1000) + 128

        url = '/v1/chat/completions'

        data = {
            "model": "google/gemma-3-4b-it",
            "messages": [
                {
                "role": "user",
                "content": question
                }
            ],
            "max_tokens": num_tokens

        }

        headers = { 'Host': '35.202.125.152',
            "Content-Type": "application/json",
        }
        
        # A POST request to the API
        r = self.client.post(url, 
                                data=json.dumps(data), 
                                headers=headers, timeout=1000)


        logger.info (f"num_tokens={num_tokens:6d}, r.status_code={r.status_code:4d}, r.reason={r.reason}")