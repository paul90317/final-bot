from utils import *
import json,os
import requests as client

def is_public_ip(s):
    return s.lower()== "public ip"

def is_request(s):
    return s.lower()== "request test"

def is_get(s):
    return s.lower()=='get'

def is_post(s):
    return s.lower()=='post'

def is_url(s):
    global gurl
    gurl=s
    return True

def on_json(**obj):
    return msg(obj['state'])

def on_ip(**obj):
    url="https://api.ipify.org/"
    res=client.get(url)
    return text_msg(res.text)

def on_wait_url(**obj):
    return text_msg('請輸入 url:')

def on_get(**obj):
    res=client.get(obj['url'])
    uid=obj['uid']
    filename=f'temp/{uid}.html'
    print(obj['url'])
    print(res.text)
    with open(filename,'w')as f:
        f.write(res.text)
    return text_msg(os.path.join(os.environ.get('HOST_URL',''),filename))

def on_post(**obj):
    res=client.post(obj['url'])
    uid=obj['uid']
    filename=f'temp/{uid}.html'
    with open(filename,'w')as f:
        f.write(res.text)
    return text_msg(os.path.join(os.environ.get('HOST_URL',''),filename))

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
        'else':'menu',
        'on_enter':on_wait_url
    },
    "post":{
        'advance':[{
            'next':'do-post',
            'condition':is_url
        }],
        'else':'menu',
        'on_enter':on_wait_url
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
    for next in check_get(machine[state],'advance',[]):
        if next['condition'](msg)==True:
            return next['next']
    return machine[state]['else']

def enter_state(**obj):
    global machine
    return machine[obj['state']]['on_enter'](state=obj['state'],uid=obj['uid'],url=obj['url'])
