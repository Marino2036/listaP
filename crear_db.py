import json
import sqlite3

# Leer archivo JSON
with open('productos.json', 'r', encoding='utf-8') as file:
    productos = json.load(file)

# Conectar a SQLite
conn = sqlite3.connect('productos.db')
cursor = conn.cursor()

# Insertar productos si no existen
for producto in productos:
    cursor.execute('SELECT COUNT(*) FROM productos WHERE id = ?', (producto['id'],))
    existe = cursor.fetchone()[0]
    if not existe:
        cursor.execute('''
            INSERT INTO productos (id, nombre, precio, categoria)
            VALUES (?, ?, ?, ?)
        ''', (producto['id'], producto['nombre'], producto['precio'], producto['categoria']))
    else:
        print(f"⚠️ Producto con ID {producto['id']} ya existe, no se insertó.")

# Guardar cambios y cerrar
conn.commit()
conn.close()

print("✅ Productos nuevos importados a la base de datos.")

