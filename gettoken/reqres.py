from locust import HttpUser, task, constant, SequentialTaskSet

class ApiUser(SequentialTaskSet):
    token = None

    @task
    def login(self):
        response = self.client.post("/api/login", json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        })
        if response.status_code == 200:
            self.token = response.json()["token"]
            print(self.token)
        else:
            response.failure("Login failed")
            print(response.status_code)
    
    @task
    def get_users(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/api/users2", headers=headers)
            print(headers)

class MyLoadTest(HttpUser):
    host = "https://reqres.in"
    tasks = [ApiUser]
    wait_time = constant(1)