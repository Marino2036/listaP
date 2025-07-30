from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import json

app = Flask(__name__)

ARCHIVO_PRODUCTOS = "productos.json"

# Productos iniciales, agregué "codigo" en algunos para ejemplo:
productos_inicial = [ 
    {"id": 1, "nombre": "Boing 500ml", "precio": 15, "categoria": "Bebidas", "codigo": "7501055301234"},
    {"id": 2, "nombre": "Boing 250ml", "precio": 9, "categoria": "Bebidas", "codigo": "7501055305678"},
    {"id": 3, "nombre": "Naranjada 600ml", "precio": 18, "categoria": "Bebidas", "codigo": "7501055309999"},
    {"id": 3, "nombre": "frutsi 125ml", "precio": 5, "categoria": "Bebidas", "codigo": "7501055387236"},
    # ... agrega códigos para los demás si quieres
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

productos = cargar_productos()

@app.route('/')
def lista_productos():
    consulta = request.args.get('q', '').lower()
    if consulta:
        resultados = [
            p for p in productos
            if consulta in p['nombre'].lower() 
            or consulta in p.get('codigo', '').lower()
        ]
    else:
        resultados = productos
    return render_template('productos.html', productos=resultados, consulta=consulta)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio'))
    categoria = request.form.get('categoria')
    # Si quieres, añade el campo 'codigo' en el formulario HTML y aquí lo capturas
    codigo = request.form.get('codigo', '')  # por defecto vacío
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
