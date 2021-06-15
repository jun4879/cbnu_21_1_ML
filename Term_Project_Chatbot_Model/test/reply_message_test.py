from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('uwNzMXdL59k3oE3fjfR9IFtO4KrDIYl9LuXgF4uOEhRD4zkv4wTvgrl/8BKV2G9VwlFTfo1CGALUe3S+sXDU+aQDNJTPyjEp7XFCb1COWzMTzjtv1CnFhaIyid+xvhDMGgq4C18YBDyVUbYWRCYu7QdB04t89/1O/w1cDnyilFU=')

try:
    line_bot_api.reply_message('uwNzMXdL59k3oE3fjfR9IFtO4KrDIYl9LuXgF4uOEhRD4zkv4wTvgrl/8BKV2G9VwlFTfo1CGALUe3S+sXDU+aQDNJTPyjEp7XFCb1COWzMTzjtv1CnFhaIyid+xvhDMGgq4C18YBDyVUbYWRCYu7QdB04t89/1O/w1cDnyilFU=',
                               TextSendMessage(text='Hello World!'))
except LineBotApiError as e:
    # error handle
    print(e)