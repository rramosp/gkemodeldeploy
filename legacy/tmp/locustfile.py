from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def hello(self):
        self.client.get("/")
