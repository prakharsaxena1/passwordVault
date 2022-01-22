# Other Standard library imports:
import os
import datetime
import random
import base64
import hashlib
import shutil

# REQUIRED MODULES
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.fernet import Fernet
    import passwordmeter
    import pyperclip
    import eel
except ModuleNotFoundError as e:
    print("Some modules that are required to run the application are not installed. Try:")
    print("pip install pillow")
    print("pip install cryptography")
    print("pip install passwordmeter")
    print("pip install pyperclip")
    print("pip install webbrowser")
    print("import eel")


eel.init("desktop")
eel.start("index.html", mode='chrome',
          host='localhost', port=27000, block=True)

# =================== CharacterSet
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./<=>?@[]^_{|}~"
X = ''.join(set(list(charset)))
# Selecting ':' as the spl. character to separate different data items when stored


def makeKEY(passgiven):  # Generating a AES Key according to the user provided password *inserts smart meme*
    salt = b''
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(passgiven))
    return key


def genPassword():  # Generating a Strong password of length = 16
    m = ''  # m is the password string
    passwordStrength = 0
    while passwordStrength <= 0.8 and len(m) < 16:
        for _ in range(16):
            m = m + X[random.randint(0, len(X)-1)]
        passwordStrength = passwordmeter.test(m)[0]
    return m


