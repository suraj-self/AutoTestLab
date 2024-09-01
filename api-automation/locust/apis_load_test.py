from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    
    @task
    def get_user_posts(self):
        url = '/posts'
        params = {'userId': 1}
        
        with self.client.get(url, params=params, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed! Status code: {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
