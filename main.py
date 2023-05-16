import requests
from requests.structures import CaseInsensitiveDict
import urllib3
import re
import pandas as pd
import json
import datetime

urllib3.disable_warnings()
# Librerías y desabilitación de advertencias.

# Ruta base del EndPoint de la WEB API.
BASE_URL = "https://localhost:44357/api"  # Para la pc
# BASE_URL = "https://localhost:7187/api"  # Para la laptop

# TODO: Hacer la identificación del usuario al endpoint "validar".
# Variable global para la autorización.
authStore = {"accessToken": ""}

# Tuplas
columnas = ("ID", "Nombre completo", "Correo", "Rol", "Estado", "Fecha registro")

# Para recorrer e imprimir los key y value del diccionario
dictRoles = {
    2: "Programador",
    3: "Administrar de BD",
    4: "Administrador",
    5: "Soporte de Aplicaciones",
    6: "Encargado de Sistemas",
    7: "Ordinario",
}

dictEstadosUsuario = {0: "Inactivo", 1: "Activo"}

# Listas
lstUsuarios = []

# Expresión regular
namePatterns = r"^([ \u00c0-\u01ffa-zA-Z'\-])+$"
emailPattern = r"^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$"
expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
passwordPattern = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{10,})"
phonePattern = r"^[0][1-9]\d{9}$|^[1-9]\d{9}$"

# Estructura del objeto usuarioDTO conforme a la WEB API.
usuario = {
    "nombre": "",
    "primer_apellido": "",
    "segundo_apellido": "",
    "fecha_nacimiento": "",
    "sexo": "",
    "celular": "",
    "correo": "",
    "contrasenia": "",
    "es_activo": "",
    "id_rol": "",
}


# Validador de expresiones regulares
# _txt es el texto a validar. _regex es el patrón de expresión regular a validar.
def RegEx(_txt, _regex):
    coincidencia = re.match(_regex, _txt)
    return bool(coincidencia)


# Función que valida una respuesta, y si es correcto, lo coloca en resultado. RegEx por función.
def validarPregunta(_patron, _pregunta="Dame un dato: "):
    global resultado
    while True:
        _fxvalor = input(_pregunta)
        coincide = re.search(_patron, _fxvalor)
        if coincide:
            resultado = int(_fxvalor)
            break
        else:
            print("*** La respuesta no es correcta. Intenta de nuevo. ***")


# Función que valida una respuesta, y si es correcto, lo coloca en resultado. RegEx por función.
def validarDatos(_patron, _pregunta="Dame un dato: "):
    global respuesta
    while True:
        if _pregunta == "Ingresa el rol: ":
            print(_pregunta)
            for x, y in dictRoles.items():
                print(f"{x} - {y}")
            _valor_ingresado = input()
        elif _pregunta == "Ingresa el estado de actividad: ":
            print(_pregunta)
            for x, y in dictEstadosUsuario.items():
                print(f"{x} - {y}")
            _valor_ingresado = input()
        else:
            _valor_ingresado = input(_pregunta)
        coincide = re.search(_patron, _valor_ingresado)
        if coincide:
            respuesta = int(_valor_ingresado)
            break
        else:
            print("*** El dato ingresado no es correcto. Intenta de nuevo. ***")
    return respuesta


def validarCampo(_patron, _tipo="text", _pregunta="Dame un dato: "):
    global respuesta
    while True:
        if _tipo == "password":
            print(_pregunta)
            print(
                "(Ingresa 10 caracteres o más; al menos una letra minúscula, una letra mayúscula, un número y un símbolo): "
            )
            _valor_ingresado = input()
        elif _tipo == "text":
            _valor_ingresado = input(_pregunta)
        coincide = re.search(_patron, _valor_ingresado)
        if coincide:
            respuesta = _valor_ingresado
            break
        else:
            print("*** El dato ingresado no es correcto. Intenta de nuevo. ***")
    return respuesta


def validarFecha():
    fecha_aceptada = False
    while not fecha_aceptada:
        try:
            fecha_actual = datetime.date.today()
            fecha_capturada = input("Fecha de nacimiento (aaaa/mm/dd): ")
            fecha_procesada = datetime.datetime.strptime(
                fecha_capturada, "%Y/%m/%d"
            ).date()
            if fecha_procesada <= fecha_actual:
                fecha_aceptada = True
            else:
                print(
                    "*** Ingresa una fecha no mayor al día de hoy. Intenta de nuevo ***"
                )
                fecha_aceptada = False
        except ValueError:
            print(
                "*** La fecha proporcionada no se encuentra en el formato indicato, favor de corregir. ***"
            )
    return fecha_procesada.strftime("%Y/%m/%d")


# Función del menú para que se ejecute cada vez al término de cada opción.
def menuPrincipal():
    print("_" * 40)
    # print("\n         *** Inovatech ***       ")
    print("\n            Menú principal           ")
    print("   [1] Consultar usuarios.")
    print("   [2] Crear usuario.")
    print("   [3] Actualizar usuario.")
    print("   [4] Eliminar usuario.")
    print("   [X] Salir.")
    print("_" * 40 + "\n")


def tituloPrincipal():
    print("_" * 40)
    print("\n         *** Inovatech ***       ")
    print("\n            Inicio de sesión           ")
    print("_" * 40 + "\n")
    print("   Ingresa tus credenciales.")
    print("_" * 40 + "\n")


# Función que obtiene con request.get un usuario específico.
def encontrarUsuario(IdUsuario):
    # TODO: En cada petición agregar un TRY, CATCH, FINALLY.
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + f"{authStore['accessToken']}"
    headers["Content-Type"] = "application/json"
    response = requests.get(
        BASE_URL + f"/Usuario/ConsultarUsuario/{IdUsuario}",
        headers=headers,
        verify=False,
    )
    json_response = response.json()

    if json_response["value"] != []:
        usuario = {}
        usuario = json_response["value"][0]
        verEntradaFormulario(usuario)
        return True
    else:
        print("\nNo se encontró el usuario con ese id")
        return False


# Función que obtiene con request.get los usuarios.
def consultarUsuarios():
    # TODO: En cada petición agregar un TRY, CATCH, FINALLY.
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + f"{authStore['accessToken']}"
    headers["Content-Type"] = "application/json"
    response = requests.get(
        BASE_URL + "/Usuario/ListarUsuario", headers=headers, verify=False
    )
    json_data = response.json()
    lstUsuarios = json_data["value"]

    if lstUsuarios:
        imprimirUsuarios(lstUsuarios)
    else:
        print("No hay usuarios registrados.")


# Función que imprime los usuarios.
def imprimirUsuarios(lstUsuarios):
    for usuario in lstUsuarios:
        print("ID:", usuario["id_usuario"])
        print("Nombre completo:", usuario["nombre_completo"])
        print("Correo:", usuario["correo"])
        print("Rol:", usuario["rol"])
        print("Activo:", usuario["activo"])
        print("Fecha registro:", usuario["fecha_registro"])
        print("")
    print("_" * 40 + "\n")


def crearUsuario(usuario):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + f"{authStore['accessToken']}"
    headers["Content-Type"] = "application/json"
    response = requests.post(
        BASE_URL + "/Usuario/GuardarUsuario",
        headers=headers,
        json=usuario,
        verify=False,
    )
    json_response = response.json()
    print("\n", json_response["value"])


def actualizarUsuario(IdUsuario, usuario):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + f"{authStore['accessToken']}"
    headers["Content-Type"] = "application/json"
    response = requests.put(
        BASE_URL + f"/Usuario/ActualizarUsuario/{IdUsuario}",
        headers=headers,
        json=usuario,
        verify=False,
    )
    json_response = response.json()
    print("\n", json_response["value"])
    # print("response: ", response.json())


def eliminarUsuario(IdUsuario):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + f"{authStore['accessToken']}"
    headers["Content-Type"] = "application/json"
    response = requests.delete(
        BASE_URL + f"/Usuario/EliminarUsuarioFisico/{IdUsuario}",
        headers=headers,
        verify=False,
    )
    json_response = response.json()
    print("\n", json_response["value"])


def verEntradaFormulario(usuario):
    print("_" * 40 + "\n")
    print("Nombre: ", usuario["nombre"])
    print("Primer apellido: ", usuario["primer_apellido"])
    print("Segundo apellido: ", usuario["segundo_apellido"])
    print("Fecha de nacimiento: ", usuario["fecha_nacimiento"])
    print("Sexo: ", usuario["sexo"])
    print("Celular: ", usuario["celular"])
    print("Correo: ", usuario["correo"])
    print("Contraseña: ", usuario["contrasenia"])
    print("Estado: ", usuario["es_activo"])
    print("Rol: ", usuario["id_rol"])


# Función de formulario para ingresar los valores al objeto usuario.
def formularioUsuario():
    usuario = {}
    usuario["nombre"] = validarCampo(namePatterns, "text", "Ingresa los nombres: ")
    usuario["primer_apellido"] = validarCampo(
        namePatterns, "text", "Ingresa el primer apellido: "
    )
    usuario["segundo_apellido"] = validarCampo(
        namePatterns, "text", "Ingresa el segundo apellido: "
    )
    usuario["fecha_nacimiento"] = validarFecha()
    usuario["sexo"] = validarCampo(
        r"^[MF]{1}$", "text", "Ingresa el sexo (F-Femenino / M-Masculino) : "
    )
    usuario["celular"] = validarCampo(phonePattern, "text", "Ingresa el celular: ")
    usuario["correo"] = validarCampo(emailPattern, "text", "Ingresa el correo:  ")
    usuario["contrasenia"] = validarCampo(
        passwordPattern, "password", "Ingresa la contraseña"
    )
    usuario["es_activo"] = validarDatos(
        r"^[0-1]{1}$", "Ingresa el estado de actividad: "
    )
    usuario["id_rol"] = validarDatos(r"^[2-7]{1}$", "Ingresa el rol: ")

    print("\nTú ingresaste en el formulario...\n")
    verEntradaFormulario(usuario)
    return usuario


def formularioInicioSesion():
    usuario = {}
    usuario["correo"] = validarCampo(expresion_regular, "text", "Correo:  ")
    usuario["contrasenia"] = validarCampo(passwordPattern, "password", "Contraseña")
    return usuario


# Función para autenticarme en la WEB API
while True:
    tituloPrincipal()
    usuario = formularioInicioSesion()
    try:
        response = requests.post(
            BASE_URL + "/Autenticacion/Validar", json=usuario, verify=False  # data
        )
        json_data = response.json()
        lstMisDatos = []

        if (
            json_data["value"]
            != "No existe información relacionada con esas credenciales."
        ):
            lstMisDatos = json_data["value"]
            authStore["accessToken"] = json_data["accessToken"]

        if lstMisDatos != []:
            print(
                "\n      Bienvenido, "
                + lstMisDatos[0]["nombre"]
                + " "
                + lstMisDatos[0]["primer_apellido"]
            )
            break
        else:
            print("\n", json_data["value"])
    except:
        print("Hubo un problema")


# Ciclo para que nos muestre el menú por cada vez que entramos y salimos de las opciones.
while True:
    menuPrincipal()
    opcion = input("¿Qué opción deseas?: ")
    respuesta = 1
    if RegEx(opcion, "^[1234xX0]{1}$"):
        if opcion == "1":
            # while respuesta == 1:
            print("_" * 40 + "\n")
            print("        [1] Consultar usuarios.")
            print("_" * 40 + "\n")

            consultarUsuarios()

        elif opcion == "2":
            while respuesta == 1:
                print("_" * 40 + "\n")
                print("        [2] Crear usuario.")
                print("_" * 40 + "\n")

                usuario = formularioUsuario()

                validarPregunta(
                    r"^[01]{1}$",
                    "\n¿Deseas guardar el usuario del formulario? \n (1-Si / 0-No): ",
                )

                if resultado == 1:
                    crearUsuario(usuario)
                    break
                else:
                    validarPregunta(
                        r"^[01]{1}$",
                        "\n¿Deseas crear un nuevo usuario? \n (1-Si / 0-No): ",
                    )
                    respuesta = resultado

        elif opcion == "3":
            while respuesta == 1:
                resultado = 0
                print("_" * 40 + "\n")
                print("        [2] Actualizar usuario.")
                print("_" * 40 + "\n")

                IdUsuario = validarDatos(
                    r"^[1-9]{1}[0-9]{0,}$",
                    "\nDime el ID del usuario que deseas actualizar: ",
                )

                encuentra = encontrarUsuario(IdUsuario)

                if encuentra:
                    print("\n")
                    usuario = formularioUsuario()
                    validarPregunta(
                        r"^[01]{1}$",
                        "\n¿Deseas actualizar el usuario del formulario? \n (1-Si / 0-No): ",
                    )

                if resultado == 1:
                    actualizarUsuario(IdUsuario, usuario)
                    break
                else:
                    validarPregunta(
                        r"^[01]{1}$",
                        "\n¿Deseas editar otro usuario? \n (1-Si / 0-No): ",
                    )
                    respuesta = resultado

        elif opcion == "4":
            while respuesta == 1:
                resultado = 0
                print("_" * 40 + "\n")
                print("        [4] Eliminar usuario.")
                print("_" * 40 + "\n")

                IdUsuario = validarDatos(
                    r"^[1-9]{1}[0-9]{0,}$",
                    "\nDime el ID del usuario que deseas eliminar: ",
                )

                encuentra = encontrarUsuario(IdUsuario)

                if encuentra:
                    validarPregunta(
                        r"^[01]{1}$",
                        "\n¿Deseas eliminar el usuario encontrado? \n (1-Si / 0-No): ",
                    )

                if resultado == 1:
                    eliminarUsuario(IdUsuario)
                    break
                else:
                    validarPregunta(
                        r"^[01]{1}$",
                        "\n¿Deseas eliminar otro usuario? \n (1-Si / 0-No): ",
                    )
                    respuesta = resultado

        elif opcion == "x" or opcion == "X":
            print("\n         *** Inovatech ***       ")
            break

        else:
            print("\n*** No has pulsado ninguna opción correcta. Intenta de nuevo. ***")

    else:
        print("\n*** Esa respuesta no es válida. Intenta de nuevo. ***")
