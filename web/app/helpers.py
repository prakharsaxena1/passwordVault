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
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(passgiven))

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
    X, pref_length, m = ''.join(set(list(charset))), int(pref["length"]), ''
    uniqueness = (pref_length//2) + 2
    mlen = len(m)
    while mlen < uniqueness:
        m = ''.join(random.choice(X) for _ in range(pref_length))
        mlen = len(set(m))
    return json.dumps({"password": m})

# API function => makes password data list
def makePassDataList(r):
    r = json.loads(r)
    site, url, login ,password = r["site"], r["url"], r["login"], r["password"]
    if site == "" or url == "" or login == "" or password == "":
        raise Exception("Invalid data provided ")
    return [ site.capitalize() , url, login, password, r["category"], r["lastUpdated"], str(uuid.uuid4()) ]

# API function => makes note data list
def makeNoteDataList(r):
    r = json.loads(r)
    title, description = r["title_AN"], r["desc_AN"]
    if title == "" and description == "":
        raise Exception("Note is empty")
    return [title, description, r["lastUpdated"], str(uuid.uuid4())]

# API function => make contact data list
def makeContactDataList(r):
    r = json.loads(r)
    if r["cname"] == "":
        raise Exception("Invalid name")
    if not (re.search(regex, r["cemail"])):  
        raise Exception("Not a valid email")
    return [ r["cname"].capitalize(), r["cemail"], str(uuid.uuid4()) ]

# API function => updates email
def emailUpdate(r):
    r = json.loads(r)
    if(re.search(regex, r["updatedEmail"])):   
        return r["updatedEmail"]
    raise Exception("Not a valid email")
    
# API function => share pass
def sharePass_enc(r):
    r = json.loads(r)
    text, method, key, contact = r["text"], r["method"], r["key"], r["contact"]
    print(r)
    # Error checking
    if (contact == "0") or (method=="UE" and key=="") or (text==""):
        raise Exception("Value error")
    
    if method == "UE":
        fernetObj = Fernet(makeKEY(f'{key+contact}'.encode()))
        return fernetObj.encrypt(text.encode()).decode()
    elif method == "SE":
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        X = ''.join(set(list(charset)))
        key = ''.join(random.choice(X) for _ in range(16)) + contact
        fernetObj1 = Fernet(makeKEY(f'{key}'.encode()))
        encryptedText1 = fernetObj1.encrypt(text.encode()).decode()
        fernetObj2 = Fernet(makeKEY(encryptedText1[0:16].encode()))
        encryptedText2 = fernetObj2.encrypt(key.encode()).decode()
        return f"{encryptedText1}ō{encryptedText2}"

def sharepassDecrypt(r):
    r = json.loads(r)
    encCode = r["encCode"]
    encType = r["encType"]
    contact = r["contact"]
    if encType == "SE":
        enc1, enc2 = encCode.split("ō")
        x = Fernet(makeKEY(f'{enc1[0:16]}'.encode()))
        key = Fernet(makeKEY(x.decrypt(enc2.encode())))
        plainFinal = key.decrypt(enc1.encode())
        return plainFinal.decode()
    elif encType == "UE":
        print(r)
        key = r["key"] + contact
        fObj = Fernet(makeKEY(key.encode()))
        plainFinal = fObj.decrypt(encCode.encode())
        return plainFinal.decode()
    
# API function => Get Password From ID
def getFromID(r, dataList):
    r = json.loads(r)
    for i in dataList:
        if i[-1]==r["id"]:
            return i
    raise Exception("No data found with given ID")

# APIs to delete data:
# Remove datalist with id
def removeDataList(r, dataList):
    r = json.loads(r)
    for i in dataList:
        if i[-1]==r["id"]:
            dataList.remove(i)
    return dataList

def getUpdatedList(d, oldList):
    for j in range(len(d)):
        if d[j] == "":
            d[j]=oldList[j]
    return d

# Update datalist with id
def updateDataList(r, dataList, service):
    r = json.loads(r)
    id = r["id"]
    temp = []
    for i in dataList:
        if i[-1]==id and service == "updatePassword":
            d = [r["site"] , r["url"], r["login"], r["password"], r["category"]]
            i = getUpdatedList(d, i) + [ r["lastUpdated"], id ]
        elif i[-1]==id and service == "updateContact":
            d = [r["cname"], r["cemail"]]
            i = getUpdatedList(d, i) + [ id ]
        elif i[-1]==id and service == "updateNote":
            d = [r["title_AN"], r["desc_AN"]]
            i = getUpdatedList(d, i) + [ r["lastUpdated"], id ]
        temp.append(i)
    return temp

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
