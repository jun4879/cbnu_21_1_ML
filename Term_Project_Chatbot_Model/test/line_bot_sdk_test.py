from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# channel access token
line_bot_api = LineBotApi('uwNzMXdL59k3oE3fjfR9IFtO4KrDIYl9LuXgF4uOEhRD4zkv4wTvgrl/8BKV2G9VwlFTfo1CGALUe3S+sXDU+aQDNJTPyjEp7XFCb1COWzMTzjtv1CnFhaIyid+xvhDMGgq4C18YBDyVUbYWRCYu7QdB04t89/1O/w1cDnyilFU=')
# channel secret
handler = WebhookHandler('4a1a6848b135f44df56004d8ef63c81f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()