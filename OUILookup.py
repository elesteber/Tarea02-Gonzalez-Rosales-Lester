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
                mac, fabricante_or = linea.split("\t", 1)  # Separa la línea en dos partes por el primer tabulador
                fabricante = fabricante_or.split("#")[0]  # Elimina la parte del fabricante que está después del # (si existe)
                fabricante = fabricante.strip()  # Elimina espacios en blanco y \n a la izquierda y derecha
                bd[mac] = fabricante
    except FileNotFoundError:           # Si no se encuentra el archivo 
        print("No se ha encontrado el archivo prueba.txt")
    except Exception as e:                  # Si ocurre cualquier otro error
        print("Ocurrio un error al leer el archivo", e)

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    mac = mac.strip()
    if mac in bd:
        return bd[mac]
    else:
        return "No se ha encontrado el fabricante"
# Función para obtener la tabla ARP
def obtener_tabla_arp():
    try:
        resultado = subprocess.check_output(['arp', '-a'], universal_newlines=True)
        return resultado  # Devuelve la tabla ARP en lugar de imprimir
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando arp")
        return None
# Función para obtener los datos de fabricación de una tarjeta de red por IP    
def obtener_datos_por_ip(ip, bd):
    tabla_arp = obtener_tabla_arp()
    if tabla_arp:
        lineas = tabla_arp.splitlines()
        for linea in lineas:
            partes = linea.split()
            if len(partes) >= 3:
                direccion_ip = partes[0]
                direccion_mac = partes[1]
                if direccion_ip == ip:
                    if direccion_mac in bd:
                        return bd[direccion_mac]
                    else:
                        return "Proveedor no encontrado"
        return "IP no encontrada en la tabla ARP"
    else:
        return "Error al obtener la tabla ARP"

def main(argv):
    ip = None
    mac = None
    arp = False

    try:
        opts, args = getopt.getopt(argv, "i:m:a", ["ip=", "mac=", "arp"])
    except getopt.GetoptError:
        print("Use: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | --help")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--ip"):
            ip = arg
        elif opt in ("--mac"):
            mac = arg
        elif opt in ("--arp"):
            arp = True
        elif opt in ("--help"):
            print("Use: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | --help")
            print("--ip : IP del host a consultar.")
            print("--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
            print("--arp: muestra los fabricantes de los host disponibles en la tabla ARP.")
            print("--help: muestra este mensaje y termina.")
            sys.exit()

    if arp:
        obtener_tabla_arp()
    elif ip:
        obtener_datos_por_ip(ip)
    elif mac:
        print("El provedor es", obtener_datos_por_mac(mac))
    else:
        print("Debe proporcionar una opción válida (--ip, --mac, --arp o --help).")

if __name__ == "__main__":
    main(sys.argv[1:])
