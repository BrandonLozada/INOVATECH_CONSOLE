import requests
import urllib3
import re
import pandas as pd
import json

urllib3.disable_warnings()
# Librerías y desabilitación de advertencias.

# Ruta base del EndPoint de la WEB API.
BASE_URL = "https://localhost:44357/api"
# BASE_URL_TEST = 'https://6448108050c25337443776cb.mockapi.io/api'

# Tuplas
columnas = ("ID", "Nombre completo", "Correo", "Rol", "Estado", "Fecha registro")

# Imprime los key y value del diccionario
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
# emailPattern = "/^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/"
# passwordPattern = "/(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{10,})/"

emailPattern = r"^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$"
passwordPattern = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{10,})"

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


# Función del menú para que se ejecute cada vez al término de cada opción.
def menuPrincipal():
    print("_" * 40)
    print("\n         *** Inovatech ***       ")
    print("\n            Menú principal           ")
    print("   [1] Consultar usuarios.")
    print("   [2] Crear usuario.")
    print("   [3] Actualizar usuario.")
    print("   [4] Eliminar usuario.")
    print("   [X] Salir.")
    print("_" * 40 + "\n")


# Función que obtiene con request.get los usuarios.
def consultarUsuarios():
    headers = {"Content-Type": "application/json"}
    response = requests.get(
        "https://localhost:44357/api/Usuario/ListarUsuario", verify=False
    )
    json_data = response.json()
    lstUsuarios = json_data["value"]
    ## json_object = json.loads(lstUsuarios)
    # json_formatted_str = json.dumps(lstUsuarios, indent=2)
    # print(json_formatted_str)
    imprimirUsuarios(lstUsuarios)


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
    response = requests.post(
        "https://localhost:44357/api/Usuario/GuardarUsuario", json=usuario, verify=False
    )
    json_response = response.json()
    print("\n", json_response["value"])

    # if response.status_code == 200 or response.status_code == 201:
    #     print('Información guardada')
    # elif response.status_code == 404:
    #     print('Not Found.')


def actualizarUsuario(IdUsuario, usuario):
    response = requests.put(
        f"https://localhost:44357/api/Usuario/ActualizarUsuario/{IdUsuario}",
        json=usuario,
        verify=False,
    )
    json_response = response.json()
    print("json_response: ", json_response["value"])
    # print("response: ", response.json())


def verEntradaFormulario(usuario):
    print("_" * 40 + "\n")
    print("Tú ingresaste en el formulario...\n")
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
    usuario["nombre"] = input("Ingresa los nombres: ")
    usuario["primer_apellido"] = input("Ingresa el primer apellido: ")
    usuario["segundo_apellido"] = input("Ingresa el segundo apellido: ")
    usuario["fecha_nacimiento"] = input("Ingresa la fecha de nacimiento: ")
    usuario["sexo"] = input("Ingresa el sexo: ")
    usuario["celular"] = input("Ingresa el celular: ")
    usuario["correo"] = validarCampo(emailPattern, "text", "Ingresa el correo:  ")
    usuario["contrasenia"] = validarCampo(
        passwordPattern, "password", "Ingresa la contraseña"
    )
    usuario["es_activo"] = validarDatos(
        r"^[0-1]{1}$", "Ingresa el estado de actividad: "
    )
    usuario["id_rol"] = validarDatos(r"^[2-7]{1}$", "Ingresa el rol: ")
    verEntradaFormulario(usuario)
    return usuario


# Ciclo para que nos muestre el menú por cada vez que entramos y salimos de las opciones.
while True:
    menuPrincipal()
    opcion = input("¿Qué opción deseas?: ")
    respuesta = 1
    if RegEx(opcion, "^[123xX0]{1}$"):
        if opcion == "1":
            # while respuesta == 1:
            print("_" * 40 + "\n")
            print("   [1] Consultar usuarios.")
            print("_" * 40 + "\n")

            consultarUsuarios()

        elif opcion == "2":
            while respuesta == 1:
                print("_" * 40 + "\n")
                print("   [2] Crear usuario.")
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
                print("_" * 40 + "\n")
                print("   [2] Actualizar usuario.")
                print("_" * 40 + "\n")

                IdUsuario = validarDatos(
                    r"^[1-9]{1}[0-9]{0,}$",
                    "\nDime el ID del usuario que deseas actualizar: ",
                )

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
                        "\n¿Deseas crear un nuevo usuario? \n (1-Si / 0-No): ",
                    )
                    respuesta = resultado

        elif opcion == "4":
            respuesta = 1
            exportar = 1
            while respuesta == 1:
                while not fecha_aceptada:
                    try:
                        fecha_actual = datetime.date.today()
                        fecha_capturada = input(
                            "\nIngresa una fecha específica para generar reporte (dd/mm/aaaa): "
                        )
                        fecha_procesada = datetime.datetime.strptime(
                            fecha_capturada, "%d/%m/%Y"
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
                try:
                    with sqlite3.connect(
                        "CosmetiqueríaFinal.db",
                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                    ) as conn:
                        mi_cursor = conn.cursor()
                        criterios = {"fecha": fecha_procesada}
                        mi_cursor.execute(
                            "SELECT * FROM ventas WHERE DATE(fecha_registro) = :fecha;",
                            criterios,
                        )
                        venta = mi_cursor.fetchall()

                        if venta:
                            print(
                                f"\n{encabezados[0]}\t{encabezados[1]}\t\t{encabezados[2]}"
                            )
                            print("---------------------------------" * 2)
                        else:
                            print(
                                f"\nNo hay registros de venta con la fecha: {fecha_capturada}"
                            )

                        for folio, monto, fecha_registro in venta:
                            print(f"{folio}\t\t", end="")
                            print("${:.2f}".format(monto) + " mxn\t", end="")
                            print(fecha_registro)
                            suma_ventas = suma_ventas + monto
                            ventas_dic[folio] = {
                                "No. Venta": folio,
                                "Monto": monto,
                                "Fecha": fecha_registro,
                            }
                        print("---------------------------------" * 2)
                except sqlite3.Error as e:
                    print(e)
                except Exception:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    if conn:
                        conn.close()
                if venta:
                    print(
                        f"\nVenta realizadas: {len(ventas_dic)} en la fecha consultada: {fecha_registro}"
                    )
                    print(
                        "La suma del importe de las ventas es de: ${:.2f}".format(
                            suma_ventas
                        )
                        + " mxn"
                    )
                validarPregunta(
                    r"^[01]{1}$",
                    "\n¿Deseas consultar otra fecha para el reporte? \n (1-Si / 0-No): ",
                )
                respuesta = resultado
                fecha_aceptada = False
                suma_ventas = 0
            if venta:
                validarPregunta(
                    r"^[01]{1}$",
                    "\n¿Deseas exportar el reporte de dicha consulta? \n (1-Si / 0-No): ",
                )
                exportar = resultado
                while exportar == 1:
                    print("\nExportando archivo...")
                    df_ventas = pd.DataFrame(ventas_dic)
                    df_ventas.to_csv(r"reporte_fecha.csv", index=True, header=None)
                    print("Exportación exitosa")
                    del df_ventas
                    exportar = 0
            # Reseteo
            estructuraArticulo = {}
            valores = {}
            ventas_dic = {}
            venta = []

        elif opcion == "x" or opcion == "X":
            print("\n         *** Inovatech ***       ")
            break

        else:
            print("\n*** No has pulsado ninguna opción correcta. Intenta de nuevo. ***")
    else:
        print("\n*** Esa respuesta no es válida. Intenta de nuevo. ***")


def getConsultarUsuarios(endPoint):
    headers = {"Content-Type": "application/json"}
    response = requests.get(BASE_URL + endPoint, verify=False)
    print(response.text)
    return response.json()


def postCrearUsuario(endPoint, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL + endPoint, json=payload, verify=False)
    print(response.json())
    if response.status_code == 200 or response.status_code == 201:
        print("Información guardada")
    elif response.status_code == 404:
        print("Not Found.")
    return response.json()


d = {"a": 1, "b": 2}
d.clear()
print(d)  # {}
