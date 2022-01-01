from utils import *
import json,os,re
import requests as client
from db import *

def is_public_ip(s):
    return s.lower()== "public ip"

def is_request(s):
    return s.lower()== "request test"

def is_get(s):
    return s.lower()=='get'

def is_post(s):
    return s.lower()=='post'

def is_try_again(s):
    return s.lower()=='再試一次'

re_url=re.compile('https?:\/\/[a-zA-Z0-9\-]+(\.[a-zA-Z0-9]+)*(\/\S*)?')
def is_url(s):
    global re_url
    return re_url.fullmatch(s)!=None

def on_json(**obj):
    return msg(obj['state'])

def on_ip(**obj):
    url="https://api.ipify.org/"
    try:
        res=client.get(url)
    except:
        return text_msg('我在人群中迷失自我...')
    return text_msg(f'我會經過 {res.text} 接送你的訊息，你也可以透過 {url} 查詢你的 Public IP')

def on_wait_url(**obj):
    return text_msg('請輸入網址')

def on_refail(**obj):
    return msg('refail')

def _success_f(cuid,content):
    filename=f'temp/{cuid}.html'
    setdb(cuid,'content',content)
    path=os.path.join(os.environ.get('HOST_URL',''),filename)
    return msg('crasuccess',{'uri':path})

def on_get(**obj):
    try:
        res=client.get(obj['url'])
    except:
        return msg('crafail')
    
    return _success_f(obj['cuid'],res.text)

def on_post(**obj):
    try:
        res=client.post(obj['url'])
    except:
        return msg('crafail')

    return _success_f(obj['cuid'],res.text)

machine={
    "menu":{
        "advance":[
            {
                "condition":is_public_ip,
                "next":"ip",
            },
            {
                "condition":is_request,
                "next":"req"
            }
        ],
        "on_enter":on_json,
        "else":'menu'
    },
    "ip":{
        "else":'menu',
        "on_enter":on_ip,
    },
    'req':{
        'advance':[
            {
                'next':'get',
                'condition':is_get
            },
            {
                'next':'post',
                'condition':is_post
            }
        ],
        'else':'menu',
        'on_enter':on_json
    },
    "get":{
        'advance':[{
            'next':'do-get',
            'condition':is_url
        }],
        'else':'refail-get',
        'on_enter':on_wait_url
    },
    "post":{
        'advance':[{
            'next':'do-post',
            'condition':is_url
        }],
        'else':'refail-post',
        'on_enter':on_wait_url
    },
    'refail-get':{
        'on_enter':on_refail,
        'advance':[{
            'next':'get',
            'condition':is_try_again
        }],
        'else':'menu'
    },
    'refail-post':{
        'on_enter':on_refail,
        'advance':[{
            'next':'post',
            'condition':is_try_again
        }],
        'else':'menu'
    },
    'do-get':{
        'on_enter':on_get,
        'else':'menu',
    },
    'do-post':{
        'on_enter':on_post,
        'else':'menu',
    }
}

def go_next(state,msg):
    global machine
    if state not in machine:
        return 'menu' 
    for next in check_get(machine[state],'advance',[]):
        if next['condition'](msg)==True:
            return next['next']
    return machine[state]['else']

def enter_state(**obj):
    global machine
    return machine[obj['state']]['on_enter'](state=obj['state'],cuid=obj['cuid'],url=obj['url'])
