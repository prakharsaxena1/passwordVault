import random
import base64
import json
import re

# REQUIRED MODULES
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.fernet import Fernet
except ModuleNotFoundError as e:
    print("Some modules that are required to run the application are not installed. Try:")
    print("pip install cryptography")
    print("pip install passwordmeter")

# GLOBALS
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# =================== Functions
def makeKEY(passgiven):  # Generating a AES Key according to the user provided password *inserts smart meme*
    salt = b''
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(passgiven))
    return key

def genPassword(pref):
    pref = json.loads(pref)
    # Default settings
    charset = "abcdefghijklmnopqrstuvwxyz"
    settings = pref["settings"]
    if settings[0] == "Y":
        charset+="!#$%&()*+,-./=?@[]^_{|}~"
    if settings[1] == "Y":
        charset+="0123456789"
    if settings[2] == "Y":
        charset+="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    X = ''.join(set(list(charset)))
    pref_length = int(pref["length"])
    m = ''
    uniqueness = (pref_length//2) + 2
    mlen= len(m)
    while mlen < uniqueness:
        m=''.join(random.choice(X) for _ in range(pref_length))
        mlen = len(set(m))
    return json.dumps({"password": m})

def makePassDataList(r):
    r = json.loads(r)
    site = r["site"]
    url = r["url"]
    login = r["login"]
    password = r["password"]
    if site == "" or url == "" or login == "" or password == "":
        raise Exception("Invalid data provided ")
    return [ r["site"], r["url"], r["login"], r["password"], r["category"], r["lastUpdated"] ]

def makeContactDataList(r):
    print(r)
    r = json.loads(r)
    cname = r["cname"]
    cemail = r["cemail"]
    if cname == "":
        raise Exception("Invalid name")
    if not (re.search(regex,cemail)):  
        raise Exception("Not a valid email")
    return [ cname, cemail ]

def emailUpdate(r):
    r = json.loads(r)
    email = r["updatedEmail"]
    if(re.search(regex,email)):   
        return email
    else:
        raise Exception("Not a valid email")
    

def httpDump(x):
    return json.dumps(x)

# Generates and returns fernet object for encryption and decryption
def getFernetObj(username, password):
    return Fernet(makeKEY(f'{username}::{password}'.encode()))

# Check login
def login_pass(username,password,checkData):
    passMatch = True
    try:
        getFernetObj(username,password).decrypt(checkData)
    except Exception as e:
        passMatch = False
    return passMatch
