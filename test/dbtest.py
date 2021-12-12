import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os,json
from hashlib import sha256

def hash(m):
    return sha256(bytes(m, 'utf-8')).hexdigest()

load_dotenv()

cred = credentials.Certificate(json.loads(os.environ['DB_KEY']))
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://linebot-temp-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref=db.reference('/sdfs')
print(ref.get())

def _hash(m):
    return sha256(bytes(m, 'utf-8')).hexdigest()

def setdb(uid,key,val):
    c=_hash(uid)
    ref=db.reference(f'/{c}')
    ref.set({
        key:val
    })

def getdb(uid,key):
    c=_hash(uid)
    ref=db.reference(f'/{c}/{key}')
    return ref.get()

print('hello')