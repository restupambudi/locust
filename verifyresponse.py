from locust import HttpUser, task, constant, between, SequentialTaskSet

class MyScript(SequentialTaskSet):
    
    @task
    def get_xml(self):
        result = self.client.get("/xml", name="XML")
        print(result)

    @task
    def get_json(self):
        expected_response = "Wake up to WonderWidgets!"

        with self.client.get("/json", name="JSON", catch_response=True) as response:
            result = True if expected_response in response.text else False
            print(self.get_json.__name__, result)
            response.success()

    @task
    def get_robot(self):
        expected_response = "*"
        result = "Fail"

        with self.client.get("/robots.txt", name="Robots", catch_response=True) as response:
            if expected_response in response.text:
                result = "Success"
                response.success()
        print(self.get_robot.__name__, result)

    @task
    def get_failure(self):
        expected_response = 404
        with self.client.get("/status/404", name="HTTP 404", catch_response=True) as response:
            if response.status_code == expected_response:
                response.failure("Got 404")
            else:
                response.success()

class MyLoadTest(HttpUser):
    wait_time = constant(1)
    host = "https://httpbin.org"
    tasks = [MyScript]