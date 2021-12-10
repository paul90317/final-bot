from utils import *
import json
import requests as client

gurl=''

def is_public_ip(s):
    return s.lower()== "public ip"
def is_request(s):
    print(s)
    return s.lower()== "request test"
def is_get(s):
    return s.lower()=='get'
def is_post(s):
    return s.lower()=='post'
def is_url(s):
    global gurl
    gurl=s
    return True

def on_json(machine,state):
    return msg(state)
def on_ip(machine,state):
    url="https://api.ipify.org/"
    res=client.get(url)
    print(res.text)
    return text_msg(res.text)
def on_wait_url(machine,state):
    return text_msg('請輸入 url:')
def on_get():
    global gurl
    res=client.get(gurl)
    print(res.text)
    return text_msg(res.text)
def on_post():
    global gurl
    res=client.post(gurl)
    print(res.text)
    return text_msg(res.text)
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
        'on_enter':on_wait_url,
        'else':'menu',
    },
    'do-post':{
        'on_enter':on_wait_url,
        'else':'menu',
    }
}

def go_next(state,msg):
    global machine
    for next in check_get(machine[state],'advance',[]):
        if next['condition'](msg)==True:
            return next['next']
    return machine[state]['else']

def enter_state(state):
    global machine
    return machine[state]['on_enter'](machine,state)
