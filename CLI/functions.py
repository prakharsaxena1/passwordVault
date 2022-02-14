# Built-in imports
import random
import base64
import os
import getpass
import hashlib

# REQUIRED MODULES
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.fernet import Fernet
except ModuleNotFoundError as e:
    print("Some modules that are required to run the application are not installed. Try:")
    print("pip install cryptography")

# GLOBALS/PATHS:
USERDATA = './data/'
ACCOUNTS_FILE = USERDATA+"accounts"
USERINFO_FOLDER = os.path.join(USERDATA, "userinfo")

# =================== Functions
def makeKEY(passgiven):  # Generating a AES Key according to the user provided password *inserts smart meme*
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(passgiven))

# Generates and returns fernet object for encryption and decryption
def getFernetObj(a, b):
    return Fernet(makeKEY(f'{a}::{b}'.encode()))

# API function => generates password
def genPassword():
    # Default settings
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./=?@[]^_{|}~"
    X, m, mlen = ''.join(set(list(charset))), '', 0
    while mlen < 12:
        m = ''.join(random.choice(X) for _ in range(16))
        mlen = len(set(m))
    return m

# Check login
def login_pass(username,password,checkData):
    passMatch = True
    try:
        getFernetObj(username,password).decrypt(checkData)
    except Exception as e:
        passMatch = False
    return passMatch

# Gives out MD5 hash of string
def getMD5Hash(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()

def loginUser():
    accounts = open(ACCOUNTS_FILE, 'r').readlines()
    username = input("Username: ")
    if username not in accounts:
        print("username does not exist, register maybe? :)")
        return None
    password = getpass.getpass("Password: ")
    userHASH = getMD5Hash(username)
    checkData = open(USERINFO_FOLDER+"/"+userHASH, 'r').readlines()[0]
    if login_pass(username, password, checkData) == True:
        print("User logged in successfully")
        return "Success"
    else:
        print("credential mismatch")
        return None

def registerUser():
    accounts = open(ACCOUNTS_FILE, 'r').readlines()
    username = input("Username: ")
    if username in accounts:
        print("username already exists, try a different one :)")
        return None
    password = getpass.getpass("Password: ")
    confirmPassword = getpass.getpass("Confirm Password: ")
    if password != confirmPassword:
        print("password mismatch!!")
        return None
    else:
        userHASH = getMD5Hash(username)
        with open(ACCOUNTS_FILE, 'a') as f:
            f.write(userHASH)
        userFolder = os.path.join(USERINFO_FOLDER, userHASH)
        os.mkdir(userFolder)
        open(userFolder+"/userdata",'w').close()
        print("Account created, now start the app again and login")        
        return "Success"

def guideUser():
    print("Go to login if you have an account in this app")
    print("Go to register if you don't have an account in this app")
    print("Still confused? Then read again")

def clearScreen():
    os.system('cls')

# Save password

# View password


if __name__ == "__main__":
    print("This module is not ment for use as a separate entity")