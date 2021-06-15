import requests, json

authorization_key = 'VSGpbFkNQaSwVl5oOkmE'
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Authorization': authorization_key
}

user_key = 'https://talk.naver.com/ct/w4pv28'
data = {
    "event": "send",
    "user": user_key,
    "textContent": {"text": "안녕"},
}

message = json.dumps(data)
response = requests.post(
    'https://clovachatbot.ncloud.com/api/chatbot/messenger/v1/query/naver',
    headers=headers,
    data=message
)
print("response status code : ", response.status_code)
print("response text : ", response.text)
