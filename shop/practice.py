import requests


login_url = "https://spark.echoindia.in/api-auth/login/"
session = requests.Session()


response = session.post(login_url, data={"email": "spal@echoindia.in", "password": "Sonupal123"})
print(response.status_code)
print(response)


# url = "https://spark.echoindia.in/api/programs/"
# response = requests.get(url)
# data = response.json()
# print(data)
