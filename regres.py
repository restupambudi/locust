from locust import HttpUser, constant, task

class MyReqRes(HttpUser):
    host = "https://reqres.in"
    wait_time = constant(1)

    @task
    def get_users(self):
        self.client.get("/api/users?page=2")

    @task
    def create_user(self):
        self.client.post("/api/users", json={"name": "morpheus", "job": "leader"})