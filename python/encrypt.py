
import binascii
import sha

def encrypt(text):
	return binascii.b2a_base64(sha.new(text).digest())

