from linebot.models import *

def check_get(m,k,e=None):
    if k in m:
        return m[k]
    return e

import json
def complex_msg(mjson):
    return FlexSendMessage(alt_text='我是機器人',contents=mjson)

def text_msg(text):
    return TextSendMessage(text=text)

def msg(state):
    try:
        with open(f"jsons/{state}.json")as f:
            mjson=json.load(f)
    except:
        return TextSendMessage(text=f"jsons/{state}.json can't open")
    print(state)
    print(mjson)
    return complex_msg(mjson)
