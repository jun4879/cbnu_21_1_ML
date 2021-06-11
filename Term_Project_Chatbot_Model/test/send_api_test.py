import requests, json

authorization_key = 'VSGpbFkNQaSwVl5oOkmE'
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Authorization': authorization_key
}

user_key = 'kjt_user_key'
data = {
    "event": "send",
    "user": user_key,
    "textContent": {"text": "hello world"},
    "inputType": "typing"
}

message = json.dumps(data)
response = requests.post(
    'https://talk.naver.com/ct/w4pv28',
    headers=headers,
    data=message
)
print(response.status_code)
print(response.text)