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
    print("Cryptography module is required to run the application and that is not installed. Try:")
    print("pip install cryptography")

# GLOBALS/PATHS:
USERDATA = './data/'
ACCOUNTS_FILE = os.path.join(USERDATA, "accounts")
USERINFO_FOLDER = os.path.join(USERDATA, "userinfo/")

if not os.path.exists(USERDATA):
    os.mkdir(USERDATA)
    os.mkdir(USERINFO_FOLDER)
    open(ACCOUNTS_FILE, 'w').close()
if os.path.exists(USERDATA) and not os.path.exists(ACCOUNTS_FILE):
    open(ACCOUNTS_FILE, 'w').close()

# =================== Functions
def makeKEY(passgiven):  # Generating a AES Key according to the user provided password *inserts smart meme*
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(passgiven))

def getFernetObj(a, b):  # Generates and returns fernet object for encryption and decryption
    return Fernet(makeKEY(f'{a}::{b}'.encode()))

def genPassword():  # Returns 16 character string to be used as a password
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./=?@[]^_{|}~"
    X, m, mlen = ''.join(set(list(charset))), '', 0
    while mlen < 12:
        m = ''.join(random.choice(X) for _ in range(16))
        mlen = len(set(m))
    return m

def getMD5Hash(x):  # Gives out MD5 hash of string
    return hashlib.md5(x.encode('utf-8')).hexdigest()

def login_pass(username,password,checkData):  # Check login
    passMatch = True
    try:
        getFernetObj(username,password).decrypt(checkData)
    except Exception as e:
        passMatch = False
    return passMatch

def loginUser():  # Login a user
    with open(ACCOUNTS_FILE, 'r') as f:
        accounts = f.readlines()
    accounts = [i.strip("\n") for i in accounts]
    username = input("Username: ")
    userHASH = getMD5Hash(username)
    if userHASH not in accounts:
        print("username does not exist, register maybe? :)")
        return None
    password = getpass.getpass("Password: ")
    checkData = open( USERINFO_FOLDER+f"{userHASH}/userdata", 'r').readlines()[0].strip("\n").encode()
    if login_pass(username, password, checkData) == True:
        app(username, password)
        return "Success"
    else:
        print("credential mismatch")
        return None

def registerUser():  # Register a user
    with open(ACCOUNTS_FILE, 'r') as f:
        accounts = f.readlines()
    accounts = [i.strip("\n") for i in accounts]
    username = input("Username: ")
    userHASH = getMD5Hash(username)
    if userHASH in accounts:
        print("username already exists, try a different one :)")
        return None
    password = getpass.getpass("Password: ")
    confirmPassword = getpass.getpass("Confirm Password: ")
    if password != confirmPassword:
        print("password mismatch!!")
        return None
    else:
        with open(ACCOUNTS_FILE, 'a') as f:
            f.write(userHASH+"\n")
        userFolder = os.path.join(USERINFO_FOLDER, userHASH)
        os.makedirs(userFolder)
        open(userFolder+"/userdata",'w').close()
        app(username, password)
        return "Success"

def guideUser():  # Display guide on terminal
    print("Go to login if you have an account in this app")
    print("Go to register if you don't have an account in this app")
    print("Still confused? Then read again")

def clearScreen(): # Clear screen
    os.system('cls')

def getID():  # Returns ID based on time of generation of password
    return round(time.time() * 1000)

def addPasswords(fernetObj, userHASH):  # Function for adding passwords
    forsite = input('Enter website name (Like facebook.com): ')
    loginID = input(f'Enter {forsite} loginID: ')
    password = input('Password(leave blank to generate a random one): ')
    if password == "":
        password = genPassword()
    data = f'{getID()}:{forsite}:{loginID}:{password}'.encode()
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    with open(dataFolder, 'a') as f:
        f.write(fernetObj.encrypt(data).decode()+"\n")

def viewPasswords(fernetObj, userHASH):  # Function for viewing passwords
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    with open(dataFolder, 'r') as f:
        for i in f.readlines():
            data = fernetObj.decrypt(i.encode()).decode().split(":")
            print(f"=====>  {data[1]}  <=====\nLoginID: {data[2]}\t\tPassword: {data[3]}\n")

def updatePasswords(fernetObj, userHASH):  # Function for updating passwords
    printForUD(fernetObj, userHASH)
    id = input("Enter password id: ")
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    pList = []
    with open(dataFolder, 'r') as f:
        for i in f.readlines():
            data = fernetObj.decrypt(i.encode()).decode().split(":")
            if data[0]==id:
                data[3] = input(f"Enter updated password: ")
            pList.append(data)
    writeToUserInfo(fernetObj, userHASH, pList)

def deletePasswords(fernetObj, userHASH):  # Function for deleting passwords
    printForUD(fernetObj, userHASH)
    id = input("Enter password id: ")
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    pList = []
    with open(dataFolder, 'r') as f:
        for i in f.readlines():
            data = fernetObj.decrypt(i.encode()).decode().split(":")
            if data[0]!=id:
                pList.append(data)
    writeToUserInfo(fernetObj, userHASH, pList)

def writeToUserInfo(fernetObj, userHASH, pList):  # Function for writing all the passwords to the userinfo
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    with open(dataFolder, 'w') as f:
        print(pList)
        for i in pList:
            f.write(fernetObj.encrypt(":".join(i).encode()).decode()+"\n")

def printForUD(fernetObj, userHASH):  # Function for printing all the fields to terminal
    dataFolder = USERINFO_FOLDER+f"{userHASH}/userdata"
    print("{:<16}  {:<50}  {:<20}  {:<16}".format('ID', 'Website', 'LoginID', 'Password'))
    with open(dataFolder, 'r') as f:
        for i in f.readlines():
            data = fernetObj.decrypt(i.encode()).decode().split(":")
            print("{:<16}  {:<50}  {:<20}  {:<16}".format(*data))

# App interface
def app(username, password):
    clearScreen()
    option = int(input("\n1. Add password\n2. View password\n3. Update password\n4. Delete password\n5. Logout\n$Option: "))
    fernetObj = getFernetObj(username, password)
    userHASH =  getMD5Hash(username)
    while(option!=5):
        if option == 1:
            addPasswords(fernetObj, userHASH)
        elif option == 2:
            viewPasswords(fernetObj, userHASH)
        elif option == 3:
            updatePasswords(fernetObj, userHASH)
        elif option == 4:
            deletePasswords(fernetObj, userHASH)
        else:
            clearScreen()
            print("Invalid input, try again")
        option = int(input("\n1. Add password\n2. View password\n3. Update password\n4. Delete password\n5. Logout\n$Option: "))
    print("Logout successful")

if __name__ == "__main__":
    print("This module is not ment for use as a separate entity")
