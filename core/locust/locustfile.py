from locust import HttpUser , task


class QuickStartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/login/" ,
            data={"email":"Fahim@gmail.com","password":"Fahim2684"}).json()

        self.client.headers = {"Authorization" : f"Bearer {response.get('access',None)}"}
        print(response.get('access'))

    @task
    def post_list(self):
        self.client.get("/api/v1/Blog/")

    @task
    def category_list(self):
        self.client.get("/api/v1/Category/")