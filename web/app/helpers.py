# Built-in imports
import random
import base64
import json
import re

# REQUIRED MODULES
try:
    import uuid
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.fernet import Fernet
except ModuleNotFoundError as e:
    print("Some modules that are required to run the application are not installed. Try:")
    print("pip install cryptography")
    print("pip install uuid")

# GLOBALS
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# =================== Functions
def makeKEY(passgiven):  # Generating a AES Key according to the user provided password *inserts smart meme*
    salt = b''
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(passgiven))
    return key

# Generates and returns fernet object for encryption and decryption
def getFernetObj(username, password):
    return Fernet(makeKEY(f'{username}::{password}'.encode()))

# API function => generates password
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

# API function => makes password data list
def makePassDataList(r):
    r = json.loads(r)
    site = r["site"]
    url = r["url"]
    login = r["login"]
    password = r["password"]
    if site == "" or url == "" or login == "" or password == "":
        raise Exception("Invalid data provided ")
    return [ r["site"].capitalize() , r["url"], r["login"], r["password"], r["category"], r["lastUpdated"], str(uuid.uuid4()) ]

# API function => makes note data list
def makeNoteDataList(r):
    r = json.loads(r)
    title, description, lastUpdated, isPinned = r["title_AN"], r["desc_AN"], r["lastUpdated"], r["isPinned"]
    if title == "" and description == "":
        raise Exception("Note is empty")
    return [title, description, lastUpdated, isPinned, str(uuid.uuid4())]

# API function => make contact data list
def makeContactDataList(r):
    r = json.loads(r)
    cname = r["cname"]
    cemail = r["cemail"]
    if cname == "":
        raise Exception("Invalid name")
    if not (re.search(regex,cemail)):  
        raise Exception("Not a valid email")
    return [ cname.capitalize(), cemail, str(uuid.uuid4()) ]

# API function => updates email
def emailUpdate(r):
    r = json.loads(r)
    email = r["updatedEmail"]
    if(re.search(regex,email)):   
        return email
    else:
        raise Exception("Not a valid email")
    
# API function => share pass
def sharePass_enc(r):
    r = json.loads(r)
    text, method, key, contact = r["text"], r["method"], r["key"], r["contact"]
    # Error checking
    if (contact == "0") or (method=="UE" and key=="") or (text==""):
        raise Exception("Value error")
    
    if method == "UE":
        fernetObj = Fernet(makeKEY(f'{key+contact}'.encode()))
        encryptedText = fernetObj.encrypt(text.encode()).decode()
        return encryptedText
    elif method == "SE":
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        X = ''.join(set(list(charset)))
        key = ''.join(random.choice(X) for _ in range(16))
        key+=contact
        fernetObj1 = Fernet(makeKEY(f'{key}'.encode()))
        encryptedText1 = fernetObj1.encrypt(text.encode()).decode()
        fernetObj2 = Fernet(makeKEY(encryptedText1[0:16].encode()))
        encryptedText2 = fernetObj2.encrypt(key.encode()).decode()
        msg = f"{encryptedText1}ō{encryptedText2}"
        return msg

# for returning JSON response
def httpDump(x):
    return json.dumps(x)

# Check login
def login_pass(username,password,checkData):
    passMatch = True
    try:
        getFernetObj(username,password).decrypt(checkData)
    except Exception as e:
        print("credential mismatch")
        passMatch = False
    return passMatch
