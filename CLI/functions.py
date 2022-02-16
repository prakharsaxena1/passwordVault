# Built-in imports
import random
import base64
import os
import getpass
import hashlib
import time

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
ACCOUNTS_FILE = os.path.join(USERDATA, "accounts")
USERINFO_FOLDER = os.path.join(USERDATA, "userinfo/")

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
        app()
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
        app()
        return "Success"

def guideUser():
    print("Go to login if you have an account in this app")
    print("Go to register if you don't have an account in this app")
    print("Still confused? Then read again")

def clearScreen():
    os.system('cls')

def getID():
    return round(time.time() * 1000)

def addPasswords(fernetObj, userHASH):
    forsite = input('Enter website name (Like facebook.com): ')
    loginID = input(f'Enter {forsite} loginID: ')
    data = f'{getID()}:{forsite}:{loginID}:{genPassword()}'.encode()
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    with open(dataFolder, 'a') as f:
        f.write(fernetObj.encrypt(data)+'\n'.encode())

def viewPasswords(fernetObj, userHASH):
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    with open(dataFolder, 'r') as f:
        for i in f.readlines():
            data = fernetObj.decrypt(i).split(":")
            print(f"=====>  {data[1]}  <=====\nLoginID: {data[2]}\t\tPassword: {data[3]}\n")

def updatePasswords():
    pass

def deletePasswords():
    pass

# App interface
def app(username, password):
    clearScreen()
    option = input("\n1. Add password\n2. View password\n3. Update password\n4. Delete password\n5. Logout\n$Option: ")
    fernetObj = getFernetObj(username, password)
    userHASH =  getMD5Hash(username)
    while(option!=5):
        if option == 1:
            addPasswords(fernetObj, userHASH)
        elif option == 2:
            viewPasswords(fernetObj, userHASH)
        elif option == 3:
            id = int(input("Enter password id: "))
            updatePasswords(id, fernetObj, userHASH)
        elif option == 4:
            id = int(input("Enter password id: "))
            deletePasswords(id, fernetObj, userHASH)
        else:
            clearScreen()
            print("Invalid input, try again")
        option = input("\n1. Add password\n2. View password\n3. Update password\n4. Delete password\n5. Logout\n$Option: ")


if __name__ == "__main__":
    print("This module is not ment for use as a separate entity")