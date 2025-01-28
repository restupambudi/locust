from locust import HttpUser, task, constant, SequentialTaskSet
import json

class ApiUser(SequentialTaskSet):
    token = None

    @task
    def login(self):
        payload = {
            "username": "emilys",
            "password": "emilyspass",
            "expiresInMins": 30
        }
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/auth/login", headers=headers, json=payload)
        if response.status_code == 200:
            self.token = response.json()["accessToken"]
        else:
            print(response.status_code)
            print("Response Text:", response.text)

    @task
    def get_users(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/auth/me", headers=headers)
            print(headers)

class MyLoadTest(HttpUser):
    host = "https://dummyjson.com"
    tasks = [ApiUser]
    wait_time = constant(1)