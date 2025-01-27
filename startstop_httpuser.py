from locust import HttpUser, task, constant, SequentialTaskSet

class MyTest(SequentialTaskSet):
    
    def on_start(self):
        self.client.get("/", name=self.on_start.__name__)
        print("Start")

    @task
    def browse_product(self):
        self.client.get("/product/OLJCESPC7Z", name=self.browse_product.__name__)
        print("Browse product")

    @task
    def cart_page(self):
        self.client.get("/cart", name=self.cart_page.__name__)
        print("Cart page")

    def on_stop(self):
        self.client.get("/", name=self.on_stop.__name__)
        print("Stop")

class LoadTest(HttpUser):
    wait_time = constant(1)
    host = "https://onlineboutique.dev"
    tasks = [MyTest]