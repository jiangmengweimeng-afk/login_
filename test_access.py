import requests

BASE_URL = "http://127.0.0.1:5000"

login_url = f"{BASE_URL}/api/v1/login/password"
login_data = {
    "username": "testuser",
    "password": "1234567"
}
print("正在登录")
login_response = requests.post(login_url, json=login_data)
print(f"登录状态码: {login_response.status_code}")
print(f"登录返回: {login_response.text}")

if login_response.status_code == 200:
    result = login_response.json()
    access_token = result.get('access_token')

    list_url = f"{BASE_URL}/api/v1/list"
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    print(f"\n正在访问: {list_url}")
    list_response = requests.get(list_url, headers=headers)
    print(f"访问状态码: {list_response.status_code}")
    print(f"返回内容: {list_response.text}")
else:
    print("登录失败， 检查用户名密码")

# session = requests.Session()

# my_refresh_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE3Nzg5MTk2MTgsInR5cGUiOiJhY2Nlc3MifQ.zUoSD-0l_9cWSFATlIocR62XD7gNhz_yygerpvQHYqQ'
# headers = {
#     "Authorization": f"Bearer {my_refresh_token}"
# }

# url = "http://127.0.0.1:5000/api/v1/access_record/list"

# print(f"正在尝试访问: {url}")
# response = session.get(url, headers=headers)

# print(f"状态码: {response.status_code}")
# print(f"返回内容: {response.text}")

