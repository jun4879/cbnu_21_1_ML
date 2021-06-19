import requests, json

class NaverEvent:
    def __init__(self, authorization):
        self.authorization_key = authorization

    def textContentComponent(self, text):
        return {
            "textContent": {
                "text": text
            }
        }

    def send_message(self, user_key, component):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': self.authorization_key
        }

        data = {
            "event": "send",
            "user": user_key
        }
        data.update(component)

        message = json.dumps(data)
        return requests.post(
            'https://clovachatbot.ncloud.com/api/chatbot/messenger/v1',  # INVOKE URL 넣으면 되나?
            headers=headers,
            data=message)

    def send_resp(self, dst_user_key, bot_resp):
        if bot_resp['Answer'] is not None:
            text = self.textContentComponent(bot_resp['Answer'])
            self.send_message(user_key=dst_user_key, component=text)

        return json.dumps({}), 200