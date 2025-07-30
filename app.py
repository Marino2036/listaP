from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import json
import unicodedata

app = Flask(__name__)

ARCHIVO_PRODUCTOS = "productos.json"

# Productos iniciales
productos_inicial = [
 {"id": 1, "nombre": "Nutri leche entera 1L", "precio": 22, "categoria": "lacteos", "codigo": ""},
    {"id": 2, "nombre": "Leche lala entera", "precio": 29, "categoria": "lacteos", "codigo": ""},
    {"id": 3, "nombre": "Leche lala deslact", "precio": 30, "categoria": "lacteos", "codigo": ""},
    {"id": 4, "nombre": "leche alpura clasica ", "precio": 26, "categoria": "lacteos", "codigo": ""},
    {"id": 5, "nombre": "Leche alpura deslact", "precio": 26, "categoria": "lacteos", "codigo": ""},
    {"id": 6, "nombre": "Leche santa clara entera ", "precio": 30, "categoria": "lacteos", "codigo": ""},
    {"id": 7, "nombre": "Leche snta clara deslacto", "precio": 30, "categoria": "lacteos", "codigo": ""},
    {"id": 8, "nombre": "coffe mate sobre", "precio": 11, "categoria": "leche polvo", "codigo": ""},
    {"id": 9, "nombre": "cafe legal sobre", "precio": 8, "categoria": "cafe", "codigo": ""},
    {"id": 10, "nombre": "nescafe sobre grande", "precio": 24, "categoria": "cafe", "codigo": ""},
    {"id": 11, "nombre": "gelatina polvo D'Gari", "precio": 13, "categoria": "gelatinas", "codigo": ""},
    {"id": 12, "nombre": "tang", "precio": 6, "categoria": "polvo/agua", "codigo": ""},
    {"id": 13, "nombre": "knor polvo sobre", "precio": 20, "categoria": "sazonadores", "codigo": ""},
    {"id": 14, "nombre": "Riko pollo polvo sobre", "precio": 22, "categoria": "sazonadores", "codigo": ""},
    {"id": 15, "nombre": "Maiz palomero 250g", "precio": 10, "categoria": "botanas", "codigo": ""},
    {"id": 16, "nombre": "Maizena atole", "precio": 0, "categoria": "atoles", "codigo": ""},
    {"id": 17, "nombre": "Royal bote", "precio": 21, "categoria": "panaderia", "codigo": ""},
    {"id": 18, "nombre": "mermelada de fresa", "precio": 30, "categoria": "mermeladas", "codigo": ""},
    {"id": 19, "nombre": "cajeta yupi", "precio": 0, "categoria": "cajeta", "codigo": ""},
    {"id": 20, "nombre": "Isadora negros", "precio": 17, "categoria": "frijoles refritos", "codigo": ""},
    {"id": 21, "nombre": "isadora bayos", "precio": 17, "categoria": "frijoles refritos", "codigo": ""},
    {"id": 22, "nombre": "Chipotles san marcos 215g", "precio": 29, "categoria": "chiles", "codigo": ""},
    {"id": 23, "nombre": "Chipotles san marcos chico", "precio": 17, "categoria": "chiles", "codigo": ""},
    {"id": 24, "nombre": "Rajas la morena", "precio": 16, "categoria": "chiles", "codigo": ""},
    {"id": 25, "nombre": "Enteros la morena", "precio": 14, "categoria": "chiles", "codigo": ""},
    {"id": 26, "nombre": "Chipotles la morena chico", "precio": 17, "categoria": "chiles", "codigo": ""},
    {"id": 27, "nombre": "Chipotles la morena grande", "precio": 32, "categoria": "chiles", "codigo": ""},
    {"id": 28, "nombre": "Chipotles la costeña grande", "precio": 26, "categoria": "chiles", "codigo": ""},
    {"id": 29, "nombre": "Chipotles la morena chico", "precio": 17, "categoria": "chiles", "codigo": ""},
    {"id": 30, "nombre": "Rajas la costeña grande", "precio": 17, "categoria": "chiles", "codigo": ""},
    {"id": 31, "nombre": "Rajas la costeña chico", "precio": 10, "categoria": "chiles", "codigo": ""},
    {"id": 32, "nombre": "Rajas la costeña grande", "precio": 17, "categoria": "chiles", "codigo": ""},
    {"id": 33, "nombre": "champiñones Herdez chico", "precio": 23, "categoria": "latas", "codigo": ""},
    {"id": 34, "nombre": "Elotes Herdez chico", "precio": 15, "categoria": "latas", "codigo": ""},
    {"id": 35, "nombre": "Rajas la costeña grande", "precio": 17, "categoria": "chiles", "codigo": ""},
    {"id": 36, "nombre": "Ensalada de verduras la costeña grande", "precio": 19, "categoria": "latas", "codigo": ""},
    {"id": 37, "nombre": "Ensalada de verduras la costeña chico", "precio": 15, "categoria": "latas", "codigo": ""},
    {"id": 38, "nombre": "Elotes la costeña grande", "precio": 20, "categoria": "latas", "codigo": ""},
    {"id": 39, "nombre": "Elotes la costeña chico", "precio": 13, "categoria": "latas", "codigo": ""},
    {"id": 40, "nombre": "Ensalada de verduras la costeña grande", "precio": 19, "categoria": "latas", "codigo": ""},
    {"id": 41, "nombre": "Frijoles refritos negros costeña", "precio": 18, "categoria": "latas", "codigo": ""},
    {"id": 42, "nombre": "Frijoles refritos bayos costeña", "precio": 18, "categoria": "latas", "codigo": ""},
    {"id": 43, "nombre": "Frijoles enteros negros costeña", "precio": 16, "categoria": "latas", "codigo": ""},
    {"id": 44, "nombre": "Frijoles enteros bayos costeña", "precio": 16, "categoria": "latas", "codigo": ""}
]

def guardar_productos(productos, archivo=ARCHIVO_PRODUCTOS):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def cargar_productos(archivo=ARCHIVO_PRODUCTOS):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return productos_inicial.copy()

def agregar_producto(productos, nombre, precio, categoria, codigo=""):
    nuevo_id = max([p["id"] for p in productos], default=0) + 1
    nuevo_producto = {"id": nuevo_id, "nombre": nombre, "precio": precio, "categoria": categoria, "codigo": codigo}
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

def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto.lower())
        if not unicodedata.combining(c)
    )

productos = cargar_productos()

@app.route('/')
def lista_productos():
    consulta_original = request.args.get('q', '')
    consulta = normalizar(consulta_original)
    if consulta:
        resultados = [
            p for p in productos
            if consulta in normalizar(p['nombre']) 
            or consulta in normalizar(p.get('codigo', ''))
        ]
    else:
        resultados = productos
    return render_template('productos.html', productos=resultados, consulta=consulta_original)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio'))
    categoria = request.form.get('categoria')
    codigo = request.form.get('codigo', '')
    agregar_producto(productos, nombre, precio, categoria, codigo)
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
        codigo = producto.get('codigo', '')
        linea = f"{producto['nombre']} - ${producto['precio']:.2f} - {producto['categoria']}"
        if codigo:
            linea += f" - Código: {codigo}"
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