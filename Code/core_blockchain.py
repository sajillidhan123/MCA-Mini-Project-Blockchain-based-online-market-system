from flask import *
import uuid
import smtplib
import hashlib
from database import *
import datetime
import codecs
import base64
import Crypto
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def get_hashed_value(previous_hash, data):
	header_bin = (str(previous_hash) + "" + str(data))
	inner_hash = hashlib.sha256(header_bin.encode()).hexdigest().encode()
	outer_hash = hashlib.sha256(inner_hash).hexdigest()
	return outer_hash

def create_block(oid, updates):
	
	#adding the checking proces to blockchain
	q = "SELECT * FROM block_chain ORDER BY block_id DESC LIMIT 1"
	print(q)
	res = select(q)
	new_hash = 0
	previous_hash = 0
	time_stamp = datetime.datetime.now()

	if res:
		previous_hash = res[0]['block_hash']

	 
	new_hash = get_hashed_value(previous_hash, time_stamp)
	password = "9874RRMFM"
	data = encrypt(str(updates), password).decode('utf-8')

	q='INSERT into block_chain values(null, "%s", "%s", "%s", "%s", "%s")'%(new_hash, data, previous_hash, oid, time_stamp)
	insert(q)
		
	return "success"

def temp_function():
	data = "sreejesh"
	password = "9874RRMFM"
	enc = encrypt(data, password)
	print(enc)
	enc = enc.decode('utf-8')
	print(enc)
	# dec = decrypt("b'gCYoUQBNO4zm8I5euNr9hQtJe/t0ck3Vh3mb1nXJ4DU='", password)
	# print(dec)


def encrypt(data, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))