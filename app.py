
from flask import Flask, request, abort, send_file

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from dotenv import load_dotenv
import os

from utils import *
from fsm import *

app = Flask(__name__)

load_dotenv()
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN",None))
# Channel Secret
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET",None))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
state={}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global state
    global machine
    uid='0'
    if event.source.type=='user':
        uid=json.loads(str(event.source))['userId']
    
    def reply(message):
        line_bot_api.reply_message(event.reply_token, message)
    text = event.message.text

    if uid not in state:
        state[uid]='menu'


    state[uid]=go_next(state[uid],text)
    reply(enter_state(
        state=state[uid],
        uid=uid,
        url=text
    ))

    if 'advance' not in machine[state[uid]]:
        state[uid]=go_next(state[uid],'')
        
    return 'OK'

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
    return 'OK'

@app.route("/")
def hello():
    return send_file("fsm.png", mimetype="image/png")

@app.route('/temp/<path:filename>',methods=['GET'])
def tempfile(filename):
    global tempfiles
    return tempfiles[filename.split('.')[0]]

import json
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
