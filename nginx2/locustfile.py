import time
import numpy as np
from locust import HttpUser, task, between
import os
import subprocess
from loguru import logger

class HttpGetUser(HttpUser):
    wait_time = between(0,1)

    @task
    def generate_content(self):

        headers = {"Host": "34.67.199.151"} # example header.

        r = self.client.get('/', headers=headers) # send Json data.
        logger.info (f"status_code={r.status_code:4d}, reason={r.reason}")
