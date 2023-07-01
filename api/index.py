from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
# from api.chatgpt import ChatGPT

import os

# 你的 LINE Channel access token'
access_token = 'hea6hI/LTc4FCcgIlR51IbcAjPWqy9QtsG5XX9Ce+4GwdfJH1EKl5/YOT3Hw4+aZOGWZSKcKPmEnUqzE4tOoBjPdvyVJJjIHwm9RN9/cWbwT7Je2GW7uNtaTSKysDrcW8F/BSEFJpywQo5Z9DXry6gdB04t89/1O/w1cDnyilFU='
# 你的 LINE Channel access token
channel_secret = '77ff5430fad4531107ca11f1c495e7dd'
# Channel Access Token
line_bot_api = LineBotApi(access_token)
# Channel Secret
line_handler = WebhookHandler(channel_secret)
#line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
#line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    if event.message.text == "說話":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
        return
    if event.message.text == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
        return
        
if __name__ == "__main__":
    app.run()
