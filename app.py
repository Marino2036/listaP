from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import json

app = Flask(__name__)

ARCHIVO_PRODUCTOS = "productos.json"

# Productos iniciales
productos_inicial = [ 

    # Bebidas
    {"id": 1, "nombre": "Boing 500ml", "precio": 15, "categoria": "Bebidas"},
    {"id": 2, "nombre": "Boing 250ml", "precio": 9, "categoria": "Bebidas"},
    {"id": 3, "nombre": "Naranjada 600ml", "precio": 18, "categoria": "Bebidas"},
    {"id": 4, "nombre": "Leche Lala 1L", "precio": 30, "categoria": "Bebidas"},
    {"id": 5, "nombre": "Refresco Coca-Cola 2L retornable", "precio": 34, "categoria": "Bebidas"},
    {"id": 6, "nombre": "Red Cola 2L", "precio": 24, "categoria": "Bebidas"},
    {"id": 7, "nombre": "Agua Bonafont 1.5L", "precio": 16, "categoria": "Bebidas"},
    {"id": 8, "nombre": "Coca cola 3L retornable", "precio": 38, "categoria": "Bebidas"},

    # Alimentos básicos
    {"id": 9, "nombre": "Arroz (1 kg)", "precio": 24, "categoria": "Alimentos básicos"},
    {"id": 10, "nombre": "Frijol negro san luis (1 kg)", "precio": 36, "categoria": "Alimentos básicos"},
    {"id": 11, "nombre": "Azúcar (1 kg)", "precio": 24, "categoria": "Alimentos básicos"},
    {"id": 12, "nombre": "Sal (1 kg)", "precio": 22, "categoria": "Alimentos básicos"},
    {"id": 13, "nombre": "Aceite Nutrioli 1L", "precio": 40, "categoria": "Alimentos básicos"},
    {"id": 14, "nombre": "Harina de trigo (1 kg)", "precio": 20, "categoria": "Alimentos básicos"},
    {"id": 15, "nombre": "Pasta para sopa (200 g)", "precio": 8, "categoria": "Alimentos básicos"},
    {"id": 16, "nombre": "Lentejas (250 g)", "precio": 10, "categoria": "Alimentos básicos"},
    {"id": 17, "nombre": "avena (1 kg)", "precio": 16, "categoria": "Alimentos básicos"},

    # Panadería
    {"id": 18, "nombre": "Tortillas (1 kg)", "precio": 18, "categoria": "Panadería"},
    {"id": 19, "nombre": "Bolillo (pieza)", "precio": 3, "categoria": "Panadería"},
    {"id": 20, "nombre": "Pan dulce (pieza)", "precio": 10, "categoria": "Panadería"},
    {"id": 21, "nombre": "Pan Bimbo chico", "precio": 38, "categoria": "Panadería"},

    # Botanas y dulces
    {"id": 22, "nombre": "Sabritas 45g", "precio": 20, "categoria": "Botanas y dulces"},
    {"id": 23, "nombre": "Takis fuego 45g", "precio": 18, "categoria": "Botanas y dulces"},
    {"id": 24, "nombre": "Galletas Emperador", "precio": 20, "categoria": "Botanas y dulces"},
    {"id": 25, "nombre": "Chicles Trident", "precio": 3.5, "categoria": "Botanas y dulces"},
    {"id": 26, "nombre": "Chocolates Carlos V grande", "precio": 10, "categoria": "Botanas y dulces"},
    {"id": 27, "nombre": "Paleta Payaso", "precio": 17, "categoria": "Botanas y dulces"},
    {"id": 28, "nombre": "Gomitas Panditas", "precio": 17, "categoria": "Botanas y dulces"},

    # Conservas y salsas
    {"id": 29, "nombre": "Salsa Valentina amarilla", "precio": 18, "categoria": "Conservas y salsas"},
    {"id": 30, "nombre": "Chiles jalapeños la costaña chica (lata)", "precio": 10, "categoria": "Conservas y salsas"},
    {"id": 31, "nombre": "Atún en agua (lata)", "precio": 21, "categoria": "Conservas y salsas"},
    {"id": 32, "nombre": "Sardinas en tomate (lata)", "precio": 40, "categoria": "Conservas y salsas"},
    {"id": 33, "nombre": "Puré de tomate chica", "precio": 12, "categoria": "Conservas y salsas"},

    # Limpieza e higiene
    {"id": 34, "nombre": "Jabón Zote grande", "precio": 12, "categoria": "Limpieza e higiene"},
    {"id": 35, "nombre": "Papel higiénico vogue(4 rollos)", "precio": 30, "categoria": "Limpieza e higiene"},
    {"id": 36, "nombre": "Shampoo sabile sobre", "precio":  4, "categoria": "Limpieza e higiene"},
    {"id": 37, "nombre": "pasta dental Colgate", "precio": 20, "categoria": "Limpieza e higiene"},
    {"id": 38, "nombre": "Cloro patitos (1 L)", "precio": 15, "categoria": "Limpieza e higiene"},
    {"id": 39, "nombre": "Detergente en polvo roma (500 g)", "precio": 22, "categoria": "Limpieza e higiene"},

    # Otros
    {"id": 40, "nombre": "Huevos (kilo)", "precio": 46, "categoria": "Otros"},
    {"id": 41, "nombre": "minino (1 kg)", "precio": 44, "categoria": "alimentos mascotas"},
    {"id": 42, "nombre": "Veladora papel", "precio": 19, "categoria": "Otros"},
    {"id": 43, "nombre": "Pilas AA (par)", "precio": 6, "categoria": "Otros"},
    {"id": 44, "nombre": "maizena natural (cajita)", "precio": 10, "categoria": "Otros"},
    {"id": 45, "nombre": "bolis", "precio": 12, "categoria": "congeladas"},
    {"id": 46, "nombre": "pure de tomate grande ", "precio": 15, "categoria": "Otros"},
    {"id": 47, "nombre": "knorr suiza (cajita)", "precio": 6, "categoria": "Otros"},
    {"id": 48, "nombre": "nescafe chico (unidad)", "precio": 11, "categoria": "Otros"},
    #nuevos 
    {"id": 49, "nombre": "Nutri leche entera", "precio": 22, "categoria": "lacteos"},
    {"id": 50, "nombre": "Leche lala entera", "precio": 29, "categoria": "lacteos"},
    {"id": 51, "nombre": "Leche lala deslact", "precio": 30, "categoria": "lacteos"},
    {"id": 52, "nombre": "leche alpura clasica ", "precio": 26, "categoria": "lacteos"},
    {"id": 53, "nombre": "Leche alpura deslact", "precio": 26, "categoria": "lacteos"},
    {"id": 54, "nombre": "Leche santa clara entera ", "precio": 30, "categoria": "lacteos"},
    {"id": 55, "nombre": "Leche snta clara deslacto", "precio": 30, "categoria": "lacteos"},
    {"id": 56, "nombre": "coffe mate sobre", "precio": 11, "categoria": "leche polvo"},
    {"id": 57, "nombre": "cafe legal sobre", "precio": 8, "categoria": "cafe"},
    {"id": 58, "nombre": "nescafe sobre grande", "precio": 24, "categoria": "cafe"},
    {"id": 59, "nombre": "gelatina polvo D'Gari", "precio": 13, "categoria": "gelatinas"},
    {"id": 60, "nombre": "tang", "precio": 6, "categoria": "polvo/agua"},
    {"id": 61, "nombre": "knor polvo sobre", "precio": 20, "categoria": "sazonadores"},
    {"id": 62, "nombre": "Riko pollo polvo sobre", "precio": 22, "categoria": "sazonadores"},
    {"id": 63, "nombre": "Maiz palomero 250g", "precio": 10, "categoria": "botanas"},
    {"id": 64, "nombre": "Maizena atole", "precio": 00, "categoria": "atoles"},
    {"id": 65, "nombre": "Royal bote", "precio": 21, "categoria": "panaderia"},
    {"id": 66, "nombre": "mermelada de fresa", "precio": 30, "categoria": "mermeladas"},
    {"id": 67, "nombre": "cajeta yupi", "precio": 00, "categoria": "cajeta"},
    {"id": 68, "nombre": "Isadora negros", "precio": 17, "categoria": "frijoles refritos"},
    {"id": 69, "nombre": "isadora bayos", "precio": 17, "categoria": "frijoles refritos"},
    {"id": 70, "nombre": "Chipotles san marcos 215g", "precio": 29, "categoria": "chiles"},
    {"id": 71, "nombre": "Chipotles san marcos chico", "precio": 17, "categoria": "chiles"},
    {"id": 72, "nombre": "Rajas la morena", "precio": 16, "categoria": "chiles"},
    {"id": 73, "nombre": "Enteros la morena", "precio": 14, "categoria": "chiles"},
    {"id": 74, "nombre": "Chipotles la morena chico", "precio": 17, "categoria": "chiles"},
    {"id": 75, "nombre": "Chipotles la morena grande", "precio": 32, "categoria": "chiles"},
    {"id": 76, "nombre": "Chipotles la costeña grande", "precio": 26, "categoria": "chiles"},
    {"id": 77, "nombre": "Chipotles la morena chico", "precio": 17, "categoria": "chiles"},
    {"id": 78, "nombre": "Rajas la costeña grande", "precio": 17, "categoria": "chiles"},
    {"id": 79, "nombre": "Rajas la costeña chico", "precio": 10, "categoria": "chiles"},
    {"id": 80, "nombre": "Rajas la costeña grande", "precio": 17, "categoria": "chiles"},
    {"id": 81, "nombre": "champiñones Herdez chico", "precio":  23, "categoria": "latas"},
    {"id": 82, "nombre": "Elotes Herdez chico", "precio": 15, "categoria": "latas"},
    {"id": 83, "nombre": "Rajas la costeña grande", "precio": 17, "categoria": "chiles"},
    {"id": 84, "nombre": "Ensalada de verduras la costeña grande", "precio": 19, "categoria": "latas"},
    {"id": 85, "nombre": "Ensalada de verduras la costeña chico", "precio": 15, "categoria": "latas"},
    {"id": 86, "nombre": "Elotes la costeña grande", "precio": 20, "categoria": "latas"},
    {"id": 87, "nombre": "Elotes la costeña chico", "precio": 13, "categoria": "latas"},
    {"id": 88, "nombre": "Ensalada de verduras la costeña grande", "precio": 19, "categoria": "latas"},
    {"id": 89, "nombre": "Frijoles refritos negros costeña", "precio": 18, "categoria": "latas"},
    {"id": 90, "nombre": "Frijoles refritos bayos costeña", "precio": 18, "categoria": "latas"},
    {"id": 91, "nombre": "Frijoles enteros negros costeña", "precio": 16, "categoria": "latas"},
    {"id": 92, "nombre": "Frijoles enteros bayos costeña", "precio": 16, "categoria": "latas"},


 ]  

# Manejo de productos
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

# Cargar lista
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

@app.route('/generar_pdf')
def generar_pdf():
    lista_productos = cargar_productos()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Lista de Productos")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Lista de Productos")

    y = 770
    pdf.setFont("Helvetica", 12)
    for producto in lista_productos:
        linea = f"{producto['nombre']} - ${producto['precio']:.2f} - {producto['categoria']}"
        pdf.drawString(50, y, linea)
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name="lista_productos.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
