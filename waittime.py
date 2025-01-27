from locust from User, task, constant, between, constant_pacing

class MyUser(User):

    wait_time = constant_pacing(3)

    @task
    def launch(self):
        time.sleep(5)
        print("Constant pacing demo")