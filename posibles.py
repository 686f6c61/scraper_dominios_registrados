import csv
import time

def leer_csv(nombre_archivo):
    """
    Lee un archivo CSV y devuelve una lista de sus contenidos.
    """
    contenido = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector, None)  # Saltar la fila de encabezado si existe
            for fila in lector:
                if len(fila) >= 2:  # Asegurarse de que la fila tiene al menos dos columnas
                    contenido.append((fila[0], fila[1]))  # Solo guardar fecha y dominio
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    return contenido

def leer_alertas(nombre_archivo):
    """
    Lee el archivo de alertas y devuelve una lista de palabras clave.
    """
    alertas = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                alerta = linea.strip()
                if alerta:
                    alertas.append(alerta)
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    return alertas

def encontrar_dominios_coincidentes(dominios, alertas):
    """
    Encuentra los dominios que contienen alguna de las palabras clave de las alertas.
    """
    coincidencias = []
    for fecha, dominio in dominios:
        for alerta in alertas:
            if alerta.lower() in dominio.lower():
                coincidencias.append((fecha, dominio, alerta))
                break  # Solo añadir una vez cada dominio
    return coincidencias

def guardar_resultados_csv(coincidencias, nombre_archivo):
    """
    Guarda solo las coincidencias encontradas en un archivo CSV.
    """
    if coincidencias:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['Fecha', 'Dominio', 'Alerta'])
            for coincidencia in coincidencias:
                escritor.writerow(coincidencia)
        print(f"Se encontraron {len(coincidencias)} coincidencias. Los resultados se han guardado en '{nombre_archivo}'.")
    else:
        print("No se encontraron coincidencias para guardar en el CSV.")

def mostrar_resultados(coincidencias):
    """
    Muestra solo las alertas encontradas.
    """
    if coincidencias:
        print(f"\nTotal de coincidencias: {len(coincidencias)}")
        print("\nAlertas encontradas:")
        for i, (fecha, dominio, alerta) in enumerate(coincidencias, 1):
            print(f"{i}. {alerta} - Fecha: {fecha}, Dominio: {dominio}")
    else:
        print("No se encontraron alertas.")

def main():
    # Leer las alertas y los dominios
    alertas = leer_alertas('alertas.csv')
    dominios = leer_csv('dominios_registrados.csv')

    print(f"Total de alertas leídas: {len(alertas)}")
    print(f"Total de dominios leídos: {len(dominios)}")
    print(f"Alertas: {alertas}")

    # Encontrar coincidencias
    start_time = time.time()
    coincidencias = encontrar_dominios_coincidentes(dominios, alertas)

    # Guardar solo las coincidencias en CSV
    guardar_resultados_csv(coincidencias, 'resultados.csv')

    # Mostrar solo las alertas encontradas
    mostrar_resultados(coincidencias)

    tiempo_total = time.time() - start_time
    print(f"\nTiempo total de procesamiento: {tiempo_total:.2f} segundos")

if __name__ == "__main__":
    main()
