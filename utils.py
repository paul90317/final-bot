from linebot.models import *

"""
{
    "alt":""
    "img_url":""
    "title":""
    "text":""
    "buttons":[
        {
            "type":"msg"
            "type":"uri"
            "label":""
            "argv":""
        }
    ]
}
"""
"""
TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
            title="是否要進行抽獎活動？",
            text="輸入生日後即獲得抽獎機會",
            actions=[
                DatetimePickerTemplateAction(
                    label="請選擇生日",
                    data="input_birthday",
                    mode='date',
                    initial='1990-01-01',
                    max='2019-03-10',
                    min='1930-01-01'
                ),
                MessageTemplateAction(
                    label="看抽獎品項",
                    text="有哪些抽獎品項呢？"
                ),
                URITemplateAction(
                    label="免費註冊享回饋",
                    uri="https://tw.shop.com/nbts/create-myaccount.xhtml?returnurl=https%3A%2F%2Ftw.shop.com%2F"
                )
            ]
        )
    )
"""
def check_get(m,k,e=None):
    if k in m:
        return m[k]
    return e

import json
def complex_msg(filelabel):
    try:
        with open(f"jsons/{filelabel}.json")as f:
            mjson=json.load(f)
    except:
        return TemplateSendMessage(
            template=ButtonsTemplate(
                title='404',
            )
        )
    
    actions=[]
    if 'buttons' in mjson:
        for button in mjson['buttons']:
            if button['type'] == 'msg':
                actions+=[
                    MessageTemplateAction(
                        label=button['label'],
                        text=button['argv']
                    )
                ]
            elif button['type'] == 'uri':
                actions+=[
                    URITemplateAction(
                        label=button['label'],
                        uri=button['argv']
                    )
                ]

    return TemplateSendMessage(
        alt_text=check_get(mjson,'alt'),
        template=ButtonsTemplate(
            thumbnail_image_url=check_get(mjson,'img_url'),
            title=check_get(mjson,'title'),
            text=check_get(mjson,'text'),
            actions=actions
        )
    )

def text_msg(text):
    return TextSendMessage(text=text)