
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
"""
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
state="user"
x=""
y=""
machine=None
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global state
    global x
    global y
    global machine
    def reply(message):
        line_bot_api.reply_message(event.reply_token, message)
    text = event.message.text
    
    if state[1:]=='x':
        x=text
    if state[1:]=='y':
        y=text
    
    next=machine.advance(state,text)
    if next==None:
        reply(text_msg('請輸入合法字串'))
        return 'OK'
    state=next
    
    if state[3:]=='out':
        reply(text_msg('x'))
        reply(text_msg('y'))
    else:
        reply(complex_msg(state))

    if machine.go_back(state)!=None:
        state=machine.go_back(state)
        if state[3:]=='out':
            reply(text_msg('x'))
            reply(text_msg('y'))
        else:
            reply(complex_msg(state))
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
"""
@app.route("/")
def hello():
    return "Hello world"
    #return send_file("fsm.png", mimetype="image/png")

import json
if __name__ == "__main__":
    """
    with open("jsons/FSM.json","r") as f:
        machine=myFSM(json.load(f))
    """
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
