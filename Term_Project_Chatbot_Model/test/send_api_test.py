import requests, json

authorization_key = 'VSGpbFkNQaSwVl5oOkmE'
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Authorization': authorization_key
}

user_key = 'jt1526'
data = {
    "event": "send",
    "user": user_key,
    "textContent": {"text": "hello talktalk test chatbot"},
}

message = json.dumps(data)
response = requests.post(
    'https://talk.naver.com/W4PV28',
    headers=headers,
    data=message
)
print("response status code : ", response.status_code)
print("response text : ", response.text)
