from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

ARCHIVO_PRODUCTOS = "productos.json"

# Lista inicial de productos (se usa si no hay archivo JSON)
productos_inicial = [
    # (tu lista completa aquí, igual que en el código que enviaste)
    {"id": 1, "nombre": "Boing 500ml", "precio": 10, "categoria": "Bebidas"},
    {"id": 2, "nombre": "Boing 250ml", "precio": 8, "categoria": "Bebidas"},
    {"id": 3, "nombre": "Naranjada 600ml", "precio": 12, "categoria": "Bebidas"},
    {"id": 4, "nombre": "Leche Lala 1L", "precio": 24, "categoria": "Bebidas"},
    {"id": 5, "nombre": "Refresco Coca-Cola 2L", "precio": 38, "categoria": "Bebidas"},
    {"id": 6, "nombre": "Red Cola 2L", "precio": 22, "categoria": "Bebidas"},
    {"id": 7, "nombre": "Agua Bonafont 1.5L", "precio": 15, "categoria": "Bebidas"},
    {"id": 8, "nombre": "Jumex lata", "precio": 10, "categoria": "Bebidas"},
    # ... sigue toda la lista ...
]

# Funciones para manejar productos y persistencia
def guardar_productos(productos, archivo=ARCHIVO_PRODUCTOS):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def cargar_productos(archivo=ARCHIVO_PRODUCTOS):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return productos_inicial.copy()

def agregar_producto(productos, nombre, precio, categoria):
    nuevo_id = max([p["id"] for p in productos], default=0) + 1
    nuevo_producto = {"id": nuevo_id, "nombre": nombre, "precio": precio, "categoria": categoria}
    productos.append(nuevo_producto)
    guardar_productos(productos)
    return nuevo_producto

def eliminar_producto(productos, id_producto):
    productos[:] = [p for p in productos if p["id"] != id_producto]
    guardar_productos(productos)

def actualizar_precio(productos, id_producto, nuevo_precio):
    for p in productos:
        if p["id"] == id_producto:
            p["precio"] = nuevo_precio
            guardar_productos(productos)
            return True
    return False

# Cargar productos al iniciar
productos = cargar_productos()

@app.route('/')
def lista_productos():
    consulta = request.args.get('q', '').lower()
    resultados = [p for p in productos if consulta in p['nombre'].lower()] if consulta else productos
    return render_template('productos.html', productos=resultados, consulta=consulta)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio'))
    categoria = request.form.get('categoria')
    agregar_producto(productos, nombre, precio, categoria)
    return redirect(url_for('lista_productos'))

@app.route('/eliminar/<int:id_producto>', methods=['POST'])
def eliminar(id_producto):
    eliminar_producto(productos, id_producto)
    return redirect(url_for('lista_productos'))

@app.route('/actualizar/<int:id_producto>', methods=['POST'])
def actualizar(id_producto):
    nuevo_precio = float(request.form.get('precio'))
    actualizar_precio(productos, id_producto, nuevo_precio)
    return redirect(url_for('lista_productos'))

if __name__ == '__main__':
    app.run(debug=True)
