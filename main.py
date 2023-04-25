import requests

BASE_URL = 'https://6448108050c25337443776cb.mockapi.io/api'

usuario = {
    'nombre': '',
    'primer_apellido': '',
    'segundo_apellido': '',
    'fecha_nacimiento': '',
    'sexo': '',
    'celular': '',
    'correo': '',
    'contrasenia': '',
    'es_activo': '',
    'id_rol': ''
}

def menuPrincipal():
    print('_' * 40)
    print("\n          *** Inovatech ***       ")
    print("\n            Menú principal           ")
    print("   [1] Consultar usuarios.")
    print("   [2] Crear usuario.")
    print("   [3] Actualizar usuario.")
    print("   [4] Eliminar usuario.")
    print("   [X] Salir.")
    print('_' * 40 + '\n')

def getConsultarUsuarios(endPoint):
    headers = {'Content-Type': 'application/json'}

    response = requests.get(BASE_URL+endPoint)
    print(response.text)
    return response.json()
    
def postCrearUsuario(endPoint, payload):
    headers = {'Content-Type': 'application/json'}

    response = requests.post(BASE_URL+endPoint, json=payload)
    print(response.json())
    return response.json()
    
# def llamadaAPI(metodo, url, payload):
#     headers = {'Content-Type': 'application/json'}

#     response = requests.post(f"{BASE_URL}/products", json=payload)
#     print(response.json())

#     response = requests.request(metodo, BASE_URL+url, headers=headers,data=payload)
#     print(response.text)
#     return response.text

def mostrarUsuarios():
    print("   [1] Consultar usuarios.")
    print('_' * 40)

    getConsultarUsuarios('/users')

def formularioUsuario():
    print('_' * 40 + '\n')
    print("   [2] Crear usuario.")
    print('_' * 40)
    usuario['nombre'] = input('Ingresa los nombres: ')
    usuario['primer_apellido'] = input('Ingresa el primer apellido: ')
    usuario['segundo_apellido'] = input('Ingresa el segundo apellido: ')
    usuario['fecha_nacimiento'] = input('Ingresa la fecha de nacimiento: ')
    usuario['sexo'] = input('Ingresa el sexo: ')
    usuario['celular'] = input('Ingresa el celular: ')
    usuario['correo'] = input('Ingresa el correo:  ')
    usuario['contrasenia'] = input('Ingresa la contraseña: ')
    usuario['es_activo'] = input('Ingresa el estado de actividad: ')
    usuario['id_rol'] = input('Ingresa el rol: ')

    print(usuario)

    postCrearUsuario('/users', usuario)
    

menuPrincipal()

mostrarUsuarios()

formularioUsuario()


