from locust import HttpUser, TaskSet, task, constant, log, SequentialTaskSet
import random
import re

class PetStore(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jsession = ""
        self.random_product = ""

    @task
    def home_page(self):
        with self.client.get("", name="T00_HomePage", catch_response=True) as response:
            if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds() < 2.0:
                response.success()
                log.setup_logging("Testing")
            else:
                response.failure("Home page took too long to load and/or text check has failed.")

    @task
    def enter_store(self):
        with self.client.get("/actions/Catalog.action", name="T10_EnterStore", catch_response=True) as response:
            for product in products:
                if product in response.text:
                    response.success()
                else:
                    response.failure("Products check failed.")
                    break
            try:
                self.jsession = re.search(r"jsessionid=(.+?)\?", response.text)
                self.jsession = self.jsession.group(1)
            except AttributeError:
                self.jsession = ""
    
    @task
    def signin_page(self):
        self.client.cookies.clear()
        url = "/actions/Account.action;jsessionid=" + self.jsession + "?signonForm="
        with self.client.get(url, name="T20_SignInPage", catch_response=True) as response:
            if "Please enter your username and password." in response.text:
                response.success()
            else:
                response.failure("Sign in page check failed.")
    
    @task
    def login(self):
        url = "/actions/Account.action"
        data = {
            "username": "j2ee",
            "password": "j2ee",
            "signon": "Login"
        }

        with self.client.post(url, data=data, name="T30_Login", catch_response=True) as response:
            if "Welcome ABC!" in response.text:
                response.success()
                try:
                    random_product = re.findall(r"Catalog.action\?viewCategory=&categoryId=(.+?)\"", response.text)
                    self.random_product = random.choice(products)
                except AttributeError:
                    self.random_product = ""
            else:
                response.failure("Login failed.")

    @task
    def random_product_page(self):
        url = "/actions/Catalog.action?viewCategory=&categoryId=" + self.random_product
        name = "T40_" + self.random_product + "_Page"
        with self.client.get(url, name=name, catch_response=True) as response:
            if self.random_product in response.text:
                response.success()
            else:
                response.failure("Product page not loaded")

    @task
    def sign_out(self):
        with self.client.get("/actions/Account.action?signoff=", name="T50_SignOut", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Sign out failed.")
        self.client.cookies.clear()

class MyLoadTest(HttpUser):
    wait_time = constant(1)
    host = "https://petstore.octoperf.com"
    tasks = [PetStore] 