from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

ARCHIVO_PRODUCTOS = "productos.json"

# Lista inicial de productos (se usa si no hay archivo JSON)
productos_inicial = [
    # Bebidas
    {"id": 1, "nombre": "Boing 500ml", "precio": 10, "categoria": "Bebidas"},
    {"id": 2, "nombre": "Boing 250ml", "precio": 8, "categoria": "Bebidas"},
    {"id": 3, "nombre": "Naranjada 600ml", "precio": 12, "categoria": "Bebidas"},
    {"id": 4, "nombre": "Leche Lala 1L", "precio": 24, "categoria": "Bebidas"},
    {"id": 5, "nombre": "Refresco Coca-Cola 2L", "precio": 38, "categoria": "Bebidas"},
    {"id": 6, "nombre": "Red Cola 2L", "precio": 22, "categoria": "Bebidas"},
    {"id": 7, "nombre": "Agua Bonafont 1.5L", "precio": 15, "categoria": "Bebidas"},
    {"id": 8, "nombre": "Jumex lata", "precio": 10, "categoria": "Bebidas"},

    # Alimentos básicos
    {"id": 9, "nombre": "Arroz (1 kg)", "precio": 24, "categoria": "Alimentos básicos"},
    {"id": 10, "nombre": "Frijol (1 kg)", "precio": 32, "categoria": "Alimentos básicos"},
    {"id": 11, "nombre": "Azúcar (1 kg)", "precio": 25, "categoria": "Alimentos básicos"},
    {"id": 12, "nombre": "Sal (1 kg)", "precio": 10, "categoria": "Alimentos básicos"},
    {"id": 13, "nombre": "Aceite Nutrioli 1L", "precio": 45, "categoria": "Alimentos básicos"},
    {"id": 14, "nombre": "Harina de trigo (1 kg)", "precio": 20, "categoria": "Alimentos básicos"},
    {"id": 15, "nombre": "Pasta para sopa (200 g)", "precio": 8, "categoria": "Alimentos básicos"},
    {"id": 16, "nombre": "Lentejas (1 kg)", "precio": 30, "categoria": "Alimentos básicos"},
    {"id": 17, "nombre": "Maíz para pozole (1 kg)", "precio": 28, "categoria": "Alimentos básicos"},

    # Panadería
    {"id": 18, "nombre": "Tortillas (1 kg)", "precio": 22, "categoria": "Panadería"},
    {"id": 19, "nombre": "Bolillo (pieza)", "precio": 3, "categoria": "Panadería"},
    {"id": 20, "nombre": "Pan dulce (pieza)", "precio": 10, "categoria": "Panadería"},
    {"id": 21, "nombre": "Pan Bimbo chico", "precio": 38, "categoria": "Panadería"},

    # Botanas y dulces
    {"id": 22, "nombre": "Sabritas 45g", "precio": 15, "categoria": "Botanas y dulces"},
    {"id": 23, "nombre": "Takis fuego 45g", "precio": 18, "categoria": "Botanas y dulces"},
    {"id": 24, "nombre": "Galletas Emperador", "precio": 10, "categoria": "Botanas y dulces"},
    {"id": 25, "nombre": "Chicles Trident", "precio": 5, "categoria": "Botanas y dulces"},
    {"id": 26, "nombre": "Chocolates Carlos V", "precio": 7, "categoria": "Botanas y dulces"},
    {"id": 27, "nombre": "Paleta Payaso", "precio": 14, "categoria": "Botanas y dulces"},
    {"id": 28, "nombre": "Gomitas Panditas", "precio": 11, "categoria": "Botanas y dulces"},

    # Conservas y salsas
    {"id": 29, "nombre": "Salsa Valentina 370ml", "precio": 18, "categoria": "Conservas y salsas"},
    {"id": 30, "nombre": "Chiles jalapeños (lata)", "precio": 16, "categoria": "Conservas y salsas"},
    {"id": 31, "nombre": "Atún en agua (lata)", "precio": 19, "categoria": "Conservas y salsas"},
    {"id": 32, "nombre": "Sardinas en tomate (lata)", "precio": 21, "categoria": "Conservas y salsas"},
    {"id": 33, "nombre": "Puré de tomate", "precio": 12, "categoria": "Conservas y salsas"},

    # Limpieza e higiene
    {"id": 34, "nombre": "Jabón Zote", "precio": 12, "categoria": "Limpieza e higiene"},
    {"id": 35, "nombre": "Papel higiénico (4 rollos)", "precio": 25, "categoria": "Limpieza e higiene"},
    {"id": 36, "nombre": "Shampoo Sedal 190ml", "precio": 28, "categoria": "Limpieza e higiene"},
    {"id": 37, "nombre": "Crema dental Colgate", "precio": 23, "categoria": "Limpieza e higiene"},
    {"id": 38, "nombre": "Cloro (1 L)", "precio": 10, "categoria": "Limpieza e higiene"},
    {"id": 39, "nombre": "Detergente en polvo (1 kg)", "precio": 26, "categoria": "Limpieza e higiene"},

    # Otros
    {"id": 40, "nombre": "Huevos (docena)", "precio": 45, "categoria": "Otros"},
    {"id": 41, "nombre": "Hielo bolsa 2kg", "precio": 18, "categoria": "Otros"},
    {"id": 42, "nombre": "Veladoras", "precio": 10, "categoria": "Otros"},
    {"id": 43, "nombre": "Pilas AA (par)", "precio": 18, "categoria": "Otros"},
    {"id": 44, "nombre": "Cigarros Marlboro (caja)", "precio": 68, "categoria": "Otros"},
    {"id": 45, "nombre": "Raspado", "precio": 10, "categoria": "Otros"},
    {"id": 46, "nombre": "Raspas sabor chamoy", "precio": 12, "categoria": "Otros"},
    {"id": 47, "nombre": "Pollo rostizado (unidad)", "precio": 95, "categoria": "Otros"},
    {"id": 48, "nombre": "Tamal (unidad)", "precio": 15, "categoria": "Otros"},
]

# Funciones para cargar/guardar y modificar lista productos
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
    actualizado = actualizar_precio(productos, id_producto, nuevo_precio)
    return redirect(url_for('lista_productos'))

if __name__ == '__main__':
    app.run(debug=True)
