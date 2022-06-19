from .models import GettingTokens
import requests


class ApiInterface():

    def __init__(self, TOKEN):
        self.token = TOKEN
        self.url = f"http://finance-tracking.ru:8002/api"

    async def create_token(self, name, email, passwd):
        # print(self.token)
        # print(self.url)
        data_send = {
            "owner" : name,
            "email_owner" : email,
            "password" : passwd
        }
        url = self.url + "/token/"
        # print(url)
        req = requests.post(url, json=data_send)
        # print(req.text)
        if req.status_code == 200:
            return GettingTokens.parse_obj(req.json())
        else:
            return False


    async def refresh_token(self, email, refresh_token):

        data_send = {
            "email" : email,
            "refresh_token" : refresh_token
        }

        url = self.url + "/token/refresh/"
        req = requests.post(url, json=data_send)

        if req.status_code == 200:
            return req.json()['access_token']
        else:
            return False

# obj = ApiInterface("sda")
# print(obj.refresh_token("asdd@mail.ru", "$2b$12$IU2g1nRCC5t0LBz1U4oJWea2hHDwp9sOERGc5iEezqUdR05ZgmhKG"))
