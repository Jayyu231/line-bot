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

line_bot_api = LineBotApi('Ajh8MOuR9E7s76jutg5EB9aeD5C/vLjMURJ3XBhaEpqUixh7nQuGbgYKUlJH9dB4u+fw1pAwlIQCHiCwL9jr0QDtaUzcdui5lK0ryJg8SZbi+2ZDQXSqmIm5aQeuOrPnz0BvnR3dSn17ML+zTgaZvQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6636e474dcf5361bd03b623b02567a9b')


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