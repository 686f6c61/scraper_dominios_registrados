# Importación de librerías necesarias

# requests: Para hacer peticiones HTTP a las páginas web
import requests

# BeautifulSoup: Para analizar y extraer datos de HTML y XML
from bs4 import BeautifulSoup

# csv: Para escribir y leer archivos CSV
import csv

# datetime y timedelta: Para manejar fechas y realizar operaciones con ellas
from datetime import datetime, timedelta

# time: Para añadir pausas en el script
import time

# os: Para operaciones relacionadas con el sistema operativo, como manejo de archivos
import os

def obtener_dominios_por_fecha(fecha_str):
    dominios = []  # Lista para almacenar todos los dominios encontrados
    parte = 1  # Contador para las partes de la página

    while True:
        try:
            # Construir la URL para cada parte de la página
            url = f"https://newly-registered-domains.abtdomain.com/{fecha_str}-com-newly-registered-domains-part-{parte}/"
            print(f"Scrapeando: {url}")
            
            # Hacer la petición HTTP
            response = requests.get(url)
            if response.status_code != 200:
                print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")
                break  # Salir del bucle si la página no se puede acceder
            
            # Parsear el contenido HTML de la página
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar el contenedor principal de los dominios
            contenedor = soup.find('div', class_='entry-container')
            
            if not contenedor:
                print(f"No se encontró el contenedor 'entry-container' en la página para la parte {parte}.")
                break  # Salir si no se encuentra el contenedor
            
            dominios_pagina = []  # Lista para almacenar los dominios de esta página
            
            # Buscar los dominios en el contenedor
            for elemento in contenedor.find_all(['p', 'div', 'span']):
                texto = elemento.get_text(strip=True)
                for linea in texto.split('\n'):
                    # Verificar si la línea es un dominio válido
                    if '.' in linea and ' ' not in linea.strip():
                        dominios_pagina.append(linea.strip())
            
            # Verificar cuántos dominios se encontraron
            if len(dominios_pagina) == 1:
                print(f"Se encontró solo 1 dominio en la parte {parte}. Finalizando la búsqueda.")
                break  # Salir si solo se encuentra un dominio (indica fin de la lista)
            elif dominios_pagina:
                print(f"Se encontraron {len(dominios_pagina)} dominios en la parte {parte}.")
                dominios.extend(dominios_pagina)
                parte += 1  # Pasar a la siguiente parte
            else:
                print(f"No se encontraron dominios en la parte {parte}. Finalizando la búsqueda.")
                break  # Salir si no se encuentran dominios
            
            time.sleep(1)  # Pausa de 1 segundo para no sobrecargar el servidor
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Finalizando el scraping...")
            break  # Salir si el usuario interrumpe el programa
        except Exception as e:
            print(f"Error al scrapear la parte {parte}: {str(e)}")
            break  # Salir si ocurre cualquier otro error
    
    return dominios  # Devolver la lista completa de dominios encontrados

def scrapear_dominios(fecha_inicio, fecha_fin):
    fecha_actual = fecha_inicio
    total_dominios = 0
    nombre_archivo = 'dominios_registrados.csv'
    
    # Abrir el archivo CSV para escribir los resultados
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['Fecha', 'Dominio'])  # Escribir encabezados
        
        # Iterar sobre el rango de fechas
        while fecha_actual <= fecha_fin:
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            print(f"\nScrapeando dominios para la fecha: {fecha_str}")
            
            # Obtener dominios para la fecha actual
            dominios = obtener_dominios_por_fecha(fecha_str)
            for dominio in dominios:
                escritor_csv.writerow([fecha_str, dominio])
                total_dominios += 1
            
            archivo_csv.flush()  # Forzar la escritura en el archivo
            os.fsync(archivo_csv.fileno())  # Asegurar que los datos se escriban en el disco
            
            print(f"Dominios guardados para {fecha_str}: {len(dominios)}")
            fecha_actual += timedelta(days=1)  # Pasar al siguiente día
    
    print(f"\nTotal de dominios guardados en el CSV: {total_dominios}")

    # Verificación adicional del archivo CSV
    if os.path.exists(nombre_archivo):
        tamaño_archivo = os.path.getsize(nombre_archivo)
        print(f"Tamaño del archivo CSV: {tamaño_archivo} bytes")
        
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv)  # Saltar la fila de encabezado
            conteo_lineas = sum(1 for _ in lector_csv)
        print(f"Número de líneas en el CSV (excluyendo encabezado): {conteo_lineas}")
    else:
        print(f"El archivo {nombre_archivo} no se ha creado correctamente.")

def obtener_fecha(mensaje):
    while True:
        fecha_str = input(mensaje)
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            print("Formato de fecha incorrecto. Por favor, use AAAA-MM-DD")

def obtener_rango_fechas():
    print("Seleccione el rango de fechas:")
    print("1. Hoy")
    print("2. Última semana")
    print("3. Últimos 15 días")
    print("4. Personalizado")
    
    opcion = input("Ingrese su opción (1-4): ")
    
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if opcion == "1":
        return hoy, hoy
    elif opcion == "2":
        return hoy - timedelta(days=7), hoy
    elif opcion == "3":
        return hoy - timedelta(days=15), hoy
    elif opcion == "4":
        fecha_inicio = obtener_fecha("Ingrese la fecha de inicio (AAAA-MM-DD): ")
        fecha_fin = obtener_fecha("Ingrese la fecha de fin (AAAA-MM-DD): ")
        return fecha_inicio, fecha_fin
    else:
        print("Opción no válida. Seleccionando 'Hoy' por defecto.")
        return hoy, hoy

# Obtener el rango de fechas del usuario
fecha_inicio, fecha_fin = obtener_rango_fechas()

# Ejecutar el scraper
try:
    scrapear_dominios(fecha_inicio, fecha_fin)
except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario. Finalizando...")

print(f"\nScraping completado para el rango {fecha_inicio.strftime('%Y-%m-%d')} - {fecha_fin.strftime('%Y-%m-%d')}.")
print("Los resultados se han guardado en 'dominios_registrados.csv'.")