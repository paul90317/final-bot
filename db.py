import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os,json
from hashlib import sha256

load_dotenv()

cred = credentials.Certificate(json.loads(os.environ['DB_KEY']))
firebase_admin.initialize_app(cred,{
    'databaseURL':os.environ['DB_URL']
})

def mhash(m):
    return sha256(bytes(m, 'utf-8')).hexdigest()

def setdb(uid,key,val):
    ref=db.reference(f'/{uid}')
    ref.set({
        key:val
    })

def getdb(uid,key):
    ref=db.reference(f'/{uid}/{key}')
    return ref.get()

print('hello')