from locust import HttpUser, task, constant, SequentialTaskSet
from readtestdata import CsvRead

class MyScript(SequentialTaskSet):
    @task
    def place_order(self):
        test_data = CsvRead("dataparameterization\\customer-data.csv").read()
        print(test_data)

        data = {
            "custname": test_data["name"],
            "phone": test_data["phone"],
            "email": test_data["email"],
            "topping": test_data["toppings"],
            "delivery": test_data["time"],
            "comment": test_data["instructions"]
        }

        name = "Order for " + test_data["name"]

        with self.client.post("/post", data=data, name=name, catch_response=True) as response:
            if response.status_code == 200 and test_data["name"] in response.text:
                response.success()
            else:
                response.failure("Failure in processing order")

class MyLoadTest(HttpUser):
    host = "https://httpbin.org"
    wait_time = constant(1)
    tasks = [MyScript]