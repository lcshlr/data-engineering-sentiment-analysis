import gevent
from locust import HttpUser, task, constant
from locust.env import Environment


class ApiStressTest(HttpUser):
    wait_time = constant(1)
    host = "http://localhost:5000"

    @task
    def prediction_stress_test(self):
        with self.client.post('/', json={'sentence': 'Test sentence'}, catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Error")


def test_locust_stress_test():
    env = Environment(user_classes=[ApiStressTest])
    env.create_local_runner()
    env.create_web_ui("localhost", 8089)
    env.runner.start(20, spawn_rate=20)
    gevent.spawn_later(60, lambda: env.runner.quit())
    env.runner.greenlet.join()
    env.web_ui.stop()

    assert env.stats.total.avg_response_time < 100
    assert env.stats.total.num_failures == 0
