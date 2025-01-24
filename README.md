# Locust Usage Guide

## Introduction

Locust is an open-source load testing tool designed for easy and efficient simulation of real-world usage scenarios. This guide will walk you through the steps to install Locust, write a test script, and run your load tests.

---

## Prerequisites

- Python 3.7 or later installed on your system.
- Basic understanding of Python programming.

---

## Step 1: Install Locust

1. Open a terminal or command prompt.

2. Run the following command to install Locust:

   ```bash
   pip install locust
   ```

3. Verify the installation by running:

   ```bash
   locust --version
   ```

---

## Step 2: Write a Locust Test Script

1. Create a new Python file, e.g., `locustfile.py`.

2. Use the following example to get started:

   ```python
   from locust import HttpUser, task, between

   class MyUser(HttpUser):
       wait_time = between(1, 3)  # Simulates user think time between requests

       @task
       def index_page(self):
           self.client.get("/")

       @task
       def about_page(self):
           self.client.get("/about")
   ```

3. Save the file in your desired directory.

---

## Step 3: Run the Locust Test

1. Open a terminal or command prompt and navigate to the directory where `locustfile.py` is saved.

2. Run the following command:

   ```bash
   locust
   ```

   or
   ```bash
   locust -f <file_name>
   ```

3. Open a web browser and navigate to `http://localhost:8089`.

4. Enter the number of users to simulate and the spawn rate (users per second).

5. Enter the target host (e.g., `http://example.com`).

6. Click the **Start Swarming** button to begin the test.

---

## Step 4: Analyze the Results

- Locust provides real-time statistics, including requests per second, response times, and failure rates.
- Use this data to analyze the performance of your application.

---