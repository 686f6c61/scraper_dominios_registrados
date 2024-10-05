import csv
import itertools

def leer_csv(nombre_archivo):
    """
    Lee un archivo CSV y devuelve una lista de frases o palabras clave.
    """
    frases = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                frases.extend(fila)  # Añade todas las palabras/frases de la fila
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    return frases

def obtener_frases_consola():
    """
    Solicita al usuario que ingrese frases o palabras clave por consola.
    """
    frases = []
    while True:
        entrada = input("Ingrese una frase o palabra clave (o 'fin' para terminar): ")
        if entrada.lower() == 'fin':
            break
        frases.append(entrada)
    return frases

def permutar_frase(frase):
    """
    Genera todas las permutaciones posibles de las palabras en una frase.
    Si es una sola palabra, la devuelve sin cambios.
    """
    palabras = frase.split()
    if len(palabras) == 1:
        return [frase]  # Si es una sola palabra, no se permuta
    return [''.join(p) for p in itertools.permutations(palabras)]

def procesar_frases(frases):
    """
    Procesa una lista de frases, generando permutaciones para cada una.
    Elimina duplicados del resultado final.
    """
    resultados = []
    for frase in frases:
        resultados.extend(permutar_frase(frase))
    return list(set(resultados))  # Elimina duplicados

def guardar_resultados(resultados, nombre_archivo):
    """
    Guarda los resultados en un archivo CSV.
    """
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        for resultado in resultados:
            escritor.writerow([resultado])
    print(f"Resultados guardados en {nombre_archivo}")

def main():
    print("Permutador de palabras y frases para alertas")
    
    # Preguntar si se quiere usar un archivo CSV
    usar_csv = input("¿Desea usar un archivo CSV? (s/n): ").lower() == 's'
    
    if usar_csv:
        nombre_archivo = input("Ingrese el nombre del archivo CSV: ")
        frases = leer_csv(nombre_archivo)
    else:
        frases = obtener_frases_consola()
    
    # Procesar las frases
    resultados = procesar_frases(frases)
    
    # Guardar resultados
    guardar_resultados(resultados, 'alertas.csv')
    
    print(f"Se generaron {len(resultados)} permutaciones.")
    print("Las alertas han sido guardadas en 'alertas.csv'.")

if __name__ == "__main__":
    main()