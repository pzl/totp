#!/usr/bin/env python

import hmac
import base64
import hashlib
import datetime
import time


#totp
interval=30 #seconds


#otp
digest=hashlib.sha1
digits=6 #number of integers supported?
secret='123456789abcdefg'



#totp
now=datetime.datetime.now()
i=time.mktime(now.timetuple())
timecode=int(i/interval)


#otp
base64_secret = base64.b32decode(secret,casefold=True)
res = []
while timecode != 0:
	res.append(chr(timecode & 0xFF))
	timecode = timecode >> 8
bytestring=''.join(reversed(res)).rjust(8,'\0') #padding=8
hmac_hash = hmac.new(
	base64_secret,
	bytestring,
	digest
).digest()

offset=ord(hmac_hash[19]) & 0xf
code = ((ord(hmac_hash[offset]) & 0x7f) << 24 |
	(ord(hmac_hash[offset + 1]) & 0xff) << 16 |
	(ord(hmac_hash[offset + 2]) & 0xff) << 8  |
	(ord(hmac_hash[offset + 3]) & 0xff))

code = code % 10 ** digits

print code
