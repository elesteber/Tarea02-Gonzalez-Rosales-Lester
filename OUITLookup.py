import subprocess
import getopt
import sys

bd = {}  # Diccionario vacío

def cargarDatos():
    global bd  # Para poder modificar la variable global
    try:
        f = open('manuf.txt', "r")
        
        for linea in f:
            linea = linea.strip()  # Elimina espacios en blanco y \n a la izquierda y derecha
            if not linea.startswith("#") and len(linea) >= 2:                       # Si la línea no empieza por # y tiene al menos dos caracteres
                mac, fabricante = linea.split("\t", 1)  # Separa la línea en dos partes por el primer tabulador
                bd[mac] = fabricante
    except FileNotFoundError:           # Si no se encuentra el archivo 
        print("No se ha encontrado el archivo manuf.txt")
    except Exception as e:                  # Si ocurre cualquier otro error
        print("Ocurrio un error al leer el archivo", e)

# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    # Implementa la lógica para obtener los datos por IP aquí
    print("Aqui su codigo para obtener los datos por ip")
    pass

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    # Implementa la lógica para obtener los datos por MAC aquí
    print("Aqui su codigo para obtener los datos por mac")
    pass

# Función para obtener la tabla ARP
def obtener_tabla_arp():
        # Implementa la lógica para procesar la tabla ARP aquí
        # Imprime la tabla ARP
    pass


def main(argv):
    ip = None

    try:
        opts, args = getopt.getopt(argv, "i", ["ip="])

    except getopt.GetoptError:
        #Modificar para coincidir con tarea
        print("Use: python OUILookup.py --ip <IP> | --Arg2 <Arg2> | --Arg3 | [--help] \n --ip : IP del host a consultar. \n --Arg2:  \n --Atg3: \n --help:")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            ip = arg

    if ip:
        obtener_datos_por_ip(ip)
    else:
        print("Debe proporcionar una opción válida (-i, -m o -a).")

if __name__ == "__main__":
    main(sys.argv[1:])
