import sqlite3
import json

def reiniciar_productos_desde_json():
    # Conexión a la base de datos
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()

    # Paso 1: Eliminar todos los productos
    cursor.execute('DELETE FROM productos')
    conn.commit()
    print("✅ Todos los productos eliminados de la base de datos.")

    # Paso 2: Cargar productos desde el JSON
    with open('productos.json', 'r', encoding='utf-8') as archivo:
        productos = json.load(archivo)

    # Paso 3: Insertar productos en la base de datos
    for producto in productos:
        cursor.execute('''
            INSERT INTO productos (id, nombre, precio, categoria, codigo)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            producto.get('id'),
            producto.get('nombre'),
            producto.get('precio'),
            producto.get('categoria'),
            producto.get('codigo', '')  # En caso de que no todos tengan código
        ))

    conn.commit()
    conn.close()
    print(f"✅ Se importaron {len(productos)} productos desde el JSON.")

# Ejecutar función (puedes llamarla al iniciar tu script si lo necesitas)
reiniciar_productos_desde_json()
