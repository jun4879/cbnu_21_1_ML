import requests, json

authorization_key = ''
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Authorization': authorization_key
}

user_key = ''
data = {
    "event": "send",
    "user": user_key,
    "textContent": {"text": "안녕"},
}

message = json.dumps(data)
response = requests.post(
    '',
    headers=headers,
    data=message
)
print("response status code : ", response.status_code)
print("response text : ", response.text)
