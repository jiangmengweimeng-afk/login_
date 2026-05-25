import requests
from .access_record.views import login_required, login_password

BASE_URL = "http://127.0.0.1:5000"

login_url = f"{BASE_URL}/api/v1/login/password"
refresh_url = f"{BASE_URL}/api/v1/refresh"
list_url = f"{BASE_URL}/api/v1/list"

login_data = {
    "username": "testuser",
    "password": "1234567"
}

session = requests.Session()
login_response = session.post(login_url, json=login_data)

if login_response.status_code == 200:
    result = login_response.json()
    access_token = result.get('access_token')

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    print(f"\n正在访问: {list_url}")
    list_response = requests.get(list_url, headers=headers)
    print(f"访问状态码: {list_response.status_code}")
    print(f"返回内容: {list_response.text}")

    refresh_response = session.post(refresh_url)
    
    if refresh_response.status_code == 200:
        new_result = refresh_response.json()
        new_access_token = new_result.get('access_token')

        new_headers = {'Authorization': f'Bearer {new_access_token}'}

        final_response = session.get(list_url, headers=new_headers)
        print(f"最终访问状态: {final_response.status_code}")
        print(f'返回内容: {final_response.text}')
    else:
        print(f'刷新失败: {refresh_response.text}')
else:
    print(f'刷新失败: {login_response.text}')
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

