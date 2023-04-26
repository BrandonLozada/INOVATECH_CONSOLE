import json
import requests
import urllib3

urllib3.disable_warnings()

# CONSULTAR USUARIOS
# headers = {'Content-Type': 'application/json'}
# response = requests.get('https://localhost:44357/api/Usuario/ListarUsuario', verify=False)
# print(response.text)

# CREAR USUARIO
# usuario = {
#     'nombre': 'Leonel',
#     'primer_apellido': 'García',
#     'segundo_apellido': 'Nuñez',
#     'fecha_nacimiento': '1975/01/27',
#     'sexo': 'M',
#     'celular': '8180250002',
#     'correo': 'leo2@gmail.com',
#     'contrasenia': 'LEOgarcia10$',
#     'es_activo': 1,
#     'id_rol': 7
# }

# response = requests.post('https://localhost:44357/api/Usuario/GuardarUsuario', json=usuario, verify=False)
# print(response.json())
# if response.status_code == 200 or response.status_code == 201:
#     print('Información guardada')
# elif response.status_code == 404:
#     print('Not Found.')

# ACTUALIZAR USUARIO
# usuario = {
#     'nombre': 'Leonel',
#     'primer_apellido': 'García',
#     'segundo_apellido': 'Nuñez de Cáceres',
#     'fecha_nacimiento': '1975/01/27',
#     'sexo': 'M',
#     'celular': '8180250000',
#     'correo': 'leo@gmail.com',
#     'contrasenia': 'LEOgarcia10$',
#     'es_activo': 1,
#     'id_rol': 7
# }

# IdUsuario = 5
# response = requests.put(f"https://localhost:44357/api/Usuario/ActualizarUsuario/{IdUsuario}", json=usuario, verify=False)
# json_response = response.json()
# print("json_response: ", json_response['value'])
# # print("response: ", response.json())

# ELIMINAR USUARIO
IdUsuario = 5

response = requests.post(f"https://localhost:44357/api/Usuario/EliminarUsuario/{IdUsuario}", verify=False)
json_response = response.json()
print("json_response: ", json_response['value'])
