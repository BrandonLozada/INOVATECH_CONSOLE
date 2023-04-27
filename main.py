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

# Listas
lstUsuarios = []

# Ciclo dentro de cada opción...


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


# Función que valida un dato, y si es correcto, lo coloca en captura. RegEx por función.
def validarDatos(_patron, _pregunta="Dame un dato: "):
    # Se especifica que captura es global.
    global captura
    while True:
        _fxvalor = input(_pregunta)
        coincide = re.search(_patron, _fxvalor)
        if coincide:
            captura = _fxvalor
            break
        else:
            print("*** El dato no es correcto. Intenta de nuevo. ***")


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


# Función que obtiene con request.get los usuarios y despues con pretty.json muestra los usuarios.
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

def imprimirUsuarios(lstUsuarios):
    print("\n")
    for usuario in lstUsuarios:
        print('ID:', usuario['id_usuario'])
        print('Nombre completo:', usuario['nombre_completo'])
        print('Correo:', usuario['correo'])
        print('Rol:', usuario['rol'])
        print('Activo:', usuario['activo'])
        print('Fecha registro:', usuario['fecha_registro'])
        print('')
    print("_" * 40 + "\n")

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
            print("_" * 40)

            consultarUsuarios()

            #     validarPregunta(r"^[1-9]{1}[0-9]{0,}$","\n¿Cuántos articulos se registrarán?: ")
            #     validarPregunta(r"^[01]{1}$","\n¿Deseas realizar otra venta? \n (1-Si / 0-No): ")

            #     respuesta = resultado
            #     cant_articulos = 0
            #     subtotal = 0
            #     fecha_aceptada = False
            # #Reseteo
            # estructuraArticulo = {}
            # valores = {}
            # lista_subtotales = []
            # venta = []

        elif opcion == "2":
            pass

        elif opcion == "3":
            # respuesta = 1
            # exportar = 1
            while respuesta == 1:
                validarPregunta(
                    r"^[1-9]{1}[0-9]{0,}$",
                    "\nDime la clave de la venta que deseas consultar: ",
                )
                clave_buscar = resultado
                try:
                    with sqlite3.connect(
                        "CosmetiqueríaFinal.db",
                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                    ) as conn:
                        mi_cursor = conn.cursor()
                        # global id_dic
                        criterios = {"folio": clave_buscar}

                        mi_cursor.execute(
                            "SELECT ven.id_venta, ven.monto, ven.fecha_registro, det.id_articulo_fk, art.descripcion, det.cantidad_comprada, art.precio, (det.cantidad_comprada * art.precio) AS SUBTOTAL \
                        FROM ventas AS ven \
                        JOIN detalle_venta AS det ON ven.id_venta = det.id_venta_fk \
                        JOIN articulos AS art ON det.id_articulo_fk = art.id_articulo \
                        WHERE ven.id_venta = :folio \
                        ORDER BY ven.id_venta;",
                            criterios,
                        )
                        venta = mi_cursor.fetchall()

                        if venta:
                            print(
                                f"\n{det_encabezados[0]}\t{det_encabezados[1]}\t{det_encabezados[2]}\t{det_encabezados[3]}\t\t{det_encabezados[4]}"
                            )
                            print("---------------------------------------" * 2)
                        else:
                            print(
                                f"\nNo hay registros de venta con la clave: {clave_buscar}"
                            )
                        id_dic = 0
                        for (
                            folio,
                            monto,
                            fecha_registro,
                            sku,
                            descripcion,
                            cantidad_comprada,
                            precio,
                            subtotal,
                        ) in venta:
                            id_dic += 1
                            print(f"{sku}\t", end="")
                            print(f"{descripcion}\t\t", end="")
                            print(f"{cantidad_comprada}\t\t", end="")
                            print("${:.2f}".format(precio) + "\t\t", end="")
                            print("${:.2f}".format(subtotal) + " mxn")
                            venta_dic[id_dic] = {
                                "No. Venta": folio,
                                "Monto": monto,
                                "Fecha": fecha_registro,
                                "Clave": sku,
                                "Articulo": descripcion,
                                "Cantidad": cantidad_comprada,
                                "Precio": precio,
                                "Subtotal": subtotal,
                            }
                        print("---------------------------------------" * 2)
                except Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    conn.close()
                if venta:
                    print(
                        f"\nVenta encontrada: #{folio} - Fecha de registro: {fecha_registro}"
                    )
                    print("El monto total fue: ${:.2f}".format(monto) + " mxn")
                validarPregunta(
                    r"^[01]{1}$", "\n¿Deseas consultar otra venta? \n (1-Si / 0-No): "
                )
                respuesta = resultado
            # if venta:
            #     validarPregunta(r"^[01]{1}$","\n¿Deseas exportar un reporte de dicha consulta? \n (1-Si / 0-No): ")
            #     exportar = resultado
            #     while exportar == 1:
            #         print("\nExportando archivo...")
            #         df_venta = pd.DataFrame(venta_dic)
            #         df_venta.to_csv (r'reporte_venta.csv',index=True, header=None)
            #         print("Exportación exitosa")
            #         del df_venta
            #         exportar = 0
            # #Reseteo
            # estructuraArticulo = {}
            # valores = {}
            # venta_dic = {}
            # venta = []

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


def mostrarUsuarios():
    getConsultarUsuarios("/Usuario/GuardarUsuario")


def formularioUsuario():
    print("_" * 40 + "\n")
    print("   [2] Crear usuario.")
    print("_" * 40)
    usuario["nombre"] = input("Ingresa los nombres: ")
    usuario["primer_apellido"] = input("Ingresa el primer apellido: ")
    usuario["segundo_apellido"] = input("Ingresa el segundo apellido: ")
    usuario["fecha_nacimiento"] = input("Ingresa la fecha de nacimiento: ")
    usuario["sexo"] = input("Ingresa el sexo: ")
    usuario["celular"] = input("Ingresa el celular: ")
    usuario["correo"] = input("Ingresa el correo:  ")
    usuario["contrasenia"] = input("Ingresa la contraseña: ")
    usuario["es_activo"] = int(input("Ingresa el estado de actividad: "))
    usuario["id_rol"] = int(input("Ingresa el rol: "))

    print(usuario)

    postCrearUsuario("/Usuario/ListarUsuario", usuario)


d = {"a": 1, "b": 2}
d.clear()
print(d)  # {}
