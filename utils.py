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

def msg(state,obj={}):
    try:
        with open(f"jsons/{state}.json")as f:
            data=f.read()
    except:
        return TextSendMessage(text=f"我的創造者似乎沒有給我 state={state} 的腳本")

    for k in obj:
        data=data.replace('{'+k+'}',obj[k])
    
    mjson=json.loads(data)
    return complex_msg(mjson)
