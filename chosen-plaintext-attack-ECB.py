import requests
from bs4 import BeautifulSoup

wordlist = "abcdefghihjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
i=1
while (True):
	data = {"username":"a"*i}
	response = requests.post('http://10.201.64.37:5000/oracle',data=data)
	soup = BeautifulSoup(response.text, 'html.parser')
	texto_cifrado = soup.find('strong').get_text()
	if i == 1:
		longitud_inicial = len(texto_cifrado)
	if len(texto_cifrado) != longitud_inicial:
		posicion_1 = i
		break
	i+=1
while(True):
	data = {"username":"a"*i}
	response = requests.post('http://10.201.64.37:5000/oracle',data=data)
	soup = BeautifulSoup(response.text, 'html.parser')
	texto_cifrado = soup.find('strong').get_text()
	if posicion_1 == i:
		longitud_inicial = len(texto_cifrado)
	if len(texto_cifrado) != longitud_inicial:
		posicion_2 = i
		break
	i+=1
tamaño_bloque = posicion_2-posicion_1
print(f"EL tamaño fijo del bloque es: {tamaño_bloque}")

offset=1
while(True):
	data = {"username":"B"*offset+"A"*tamaño_bloque*2}
	respuesta=requests.post('http://10.201.64.37:5000/oracle',data=data)
	soup = BeautifulSoup(respuesta.text, 'html.parser')
	texto_cifrado = soup.find('strong').get_text()
	partes = [texto_cifrado[i:i+tamaño_bloque*2] for i in range(0,len(texto_cifrado),tamaño_bloque*2)]
	n_bloques = len(partes)
	if n_bloques != len(set(partes)):
		print(f"El offset viene a ser : {offset}")
		break
	offset +=1

sufijo = ""
for j in range(1,16):
	data = {"username":"B"*offset+"A"*(tamaño_bloque-j)}
	respuesta=requests.post('http://10.201.64.37:5000/oracle',data=data)
	soup = BeautifulSoup(respuesta.text, 'html.parser')
	texto_cifrado = soup.find('strong').get_text()
	partes = [texto_cifrado[i:i+tamaño_bloque*2] for i in range(0,len(texto_cifrado),tamaño_bloque*2)]
	busqueda = partes[1]
	for i in wordlist:
		data = {"username":"B"*offset+"A"*(tamaño_bloque-j)+f"{sufijo}{i}"}
		respuesta=requests.post('http://10.201.64.37:5000/oracle',data=data)
		soup = BeautifulSoup(respuesta.text, 'html.parser')
		texto_cifrado = soup.find('strong').get_text()
		partes = [texto_cifrado[i:i+tamaño_bloque*2] for i in range(0,len(texto_cifrado),tamaño_bloque*2)]
		if busqueda == partes[1]:
			sufijo +=i
			break
print(f"El sufijo agregado a a nuestra entrada vienen a ser: {sufijo}")
