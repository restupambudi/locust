from locust import HttpUser, task, constant, SequentialTaskSet
import logging

class PetStore(SequentialTaskSet):
    @task
    def home_page(self):
        with self.client.get("/", name="T00_HomePage", catch_response=True) as response:
            if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds() < 2.0:
                response.success()
                logging.info("Home page loaded successfully.")
            else:
                response.failure("Home page took too long to load and/or text check has failed.")
                logging.error("Home page did not load successfully.")

class MyLoadTest(HttpUser):
    tasks = [PetStore]
    wait_time = constant(1)
    host = "https://petstore.octoperf.com"