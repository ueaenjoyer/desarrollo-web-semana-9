# ============================================
# productos.py - Persistencia en Archivos
# Semana 12 - TechByte
# ============================================
#
# Este módulo implementa tres mecanismos de persistencia con archivos:
#
# 1. TXT  → Usando open() en modo lectura/escritura
# 2. JSON → Usando la librería json (json.dump / json.load)
# 3. CSV  → Usando la librería csv (csv.writer / csv.reader)
#
# Cada función escribe o lee datos del directorio inventario/data/
# ============================================

import os
import json
import csv

# Ruta absoluta al directorio de datos
# __file__ = ruta al archivo actual (productos.py)
# os.path.dirname() obtiene el directorio que contiene el archivo
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Rutas completas a cada archivo de datos
ARCHIVO_TXT  = os.path.join(DATA_DIR, 'datos.txt')
ARCHIVO_JSON = os.path.join(DATA_DIR, 'datos.json')
ARCHIVO_CSV  = os.path.join(DATA_DIR, 'datos.csv')

# Campos del CSV (encabezados)
CAMPOS_CSV = ['nombre', 'precio', 'cantidad', 'descripcion']


# ============================================
# PERSISTENCIA CON TXT
# Se usa open() con modos 'a' (append) y 'r' (read)
# Cada registro se guarda en una línea con separadores
# ============================================

def guardar_txt(datos):
    """
    Guarda un registro en el archivo TXT usando open() en modo 'append'.
    Cada línea del archivo representa un registro con campos separados por '|'.

    Formato de cada línea:
        nombre|precio|cantidad|descripcion

    Args:
        datos (dict): Diccionario con 'nombre', 'precio', 'cantidad', 'descripcion'.
    """
    linea = f"{datos['nombre']}|{datos['precio']}|{datos['cantidad']}|{datos.get('descripcion', '')}\n"
    # 'a' → modo append: agrega al final sin borrar el contenido existente
    # encoding='utf-8' → soporte para caracteres especiales (ñ, tildes, etc.)
    with open(ARCHIVO_TXT, 'a', encoding='utf-8') as f:
        f.write(linea)


def leer_txt():
    """
    Lee todos los registros del archivo TXT.

    Returns:
        list: Lista de diccionarios con los datos de cada registro.
              Retorna lista vacía si el archivo no existe o está vacío.
    """
    registros = []

    # Verificamos que el archivo existe antes de intentar leerlo
    if not os.path.exists(ARCHIVO_TXT):
        return registros

    # 'r' → modo lectura
    with open(ARCHIVO_TXT, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()  # Eliminamos saltos de línea y espacios
            if linea:              # Ignoramos líneas vacías
                partes = linea.split('|')
                if len(partes) == 4:
                    registros.append({
                        'nombre': partes[0],
                        'precio': partes[1],
                        'cantidad': partes[2],
                        'descripcion': partes[3]
                    })
    return registros


# ============================================
# PERSISTENCIA CON JSON
# Se usa la librería json: json.dump() para escribir y json.load() para leer
# Los datos se almacenan como una lista de diccionarios
# ============================================

def guardar_json(datos):
    """
    Guarda un registro en el archivo JSON.

    Primero lee los datos existentes, agrega el nuevo registro,
    y escribe todo de vuelta al archivo usando json.dump().

    Args:
        datos (dict): Diccionario con los datos del producto.
    """
    # Leemos los datos existentes (o lista vacía si no hay nada)
    registros = leer_json()

    # Convertimos precio y cantidad a tipos correctos
    nuevo = {
        'nombre': datos['nombre'],
        'precio': float(datos['precio']),
        'cantidad': int(datos['cantidad']),
        'descripcion': datos.get('descripcion', '')
    }

    # Agregamos el nuevo registro a la lista
    registros.append(nuevo)

    # Guardamos toda la lista de vuelta al archivo JSON
    # indent=4 → formato legible con indentación de 4 espacios
    # ensure_ascii=False → permite caracteres UTF-8 (ñ, tildes)
    with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)


def leer_json():
    """
    Lee todos los registros del archivo JSON usando json.load().

    Returns:
        list: Lista de diccionarios con los datos almacenados.
              Retorna lista vacía si el archivo no existe o está vacío.
    """
    if not os.path.exists(ARCHIVO_JSON):
        return []

    with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
        contenido = f.read().strip()
        if not contenido:
            return []
        # json.load() convierte el texto JSON a estructura Python
        return json.loads(contenido)


# ============================================
# PERSISTENCIA CON CSV
# Se usa la librería csv: csv.writer y csv.reader
# Los datos se almacenan con la primera fila como encabezado
# ============================================

def guardar_csv(datos):
    """
    Guarda un registro en el archivo CSV usando csv.writer.

    Agrega una nueva fila al archivo CSV sin borrar las existentes.
    El archivo ya tiene la fila de encabezados (creada inicialmente).

    Args:
        datos (dict): Diccionario con los datos del producto.
    """
    # 'a' → modo append; newline='' → evita líneas en blanco extra en Windows
    with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Escribimos una fila con los valores en el orden de CAMPOS_CSV
        writer.writerow([
            datos['nombre'],
            datos['precio'],
            datos['cantidad'],
            datos.get('descripcion', '')
        ])


def leer_csv():
    """
    Lee todos los registros del archivo CSV usando csv.reader.

    Returns:
        list: Lista de diccionarios con los datos de cada fila.
              Retorna lista vacía si el archivo no existe o está vacío.
    """
    registros = []

    if not os.path.exists(ARCHIVO_CSV):
        return registros

    with open(ARCHIVO_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Leemos y descartamos la primera fila (encabezados)
        try:
            encabezados = next(reader)
        except StopIteration:
            return registros  # Archivo vacío

        # Iteramos sobre las filas restantes
        for fila in reader:
            if fila and len(fila) == 4:  # Verificamos que la fila tenga datos
                registros.append({
                    'nombre': fila[0],
                    'precio': fila[1],
                    'cantidad': fila[2],
                    'descripcion': fila[3]
                })

    return registros
