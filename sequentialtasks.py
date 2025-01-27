from locust import SequentialTaskSet, HttpUser, task, constant

class MySeqTask(SequentialTaskSet):
    
    @task
    def get_status(self):
        self.client.get("/200")
        print("Status code: 200")

    @task
    def second_task(self):
        self.client.get("/500")
        print("Status code: 500")

class MyLoadTest(HttpUser):
    
    host = "https://http.cat"
    wait_time = constant(1)
    tasks = [MySeqTask]