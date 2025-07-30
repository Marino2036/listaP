from flask import Flask, render_template, request, redirect, send_file
import json
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

DB_FILE = 'productos.json'

datos_iniciales = [
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
]

if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos_iniciales, f, indent=4, ensure_ascii=False)

def cargar_productos():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_productos(productos):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    productos = cargar_productos()
    categorias = sorted(set(p['categoria'] for p in productos))
    return render_template('productos.html', productos=productos, categorias=categorias)

@app.route('/agregar', methods=['POST'])
def agregar():
    productos = cargar_productos()
    nuevo = {
        'id': productos[-1]['id'] + 1 if productos else 1,
        'nombre': request.form['nombre'],
        'precio': float(request.form['precio']),
        'categoria': request.form['categoria'],
        'codigo': request.form.get('codigo', '')
    }
    productos.append(nuevo)
    guardar_productos(productos)
    return redirect('/')

@app.route('/buscar')
def buscar():
    termino = request.args.get('q', '').lower()
    productos = cargar_productos()
    resultados = [p for p in productos if termino in p['nombre'].lower() or termino in p.get('codigo', '')]
    categorias = sorted(set(p['categoria'] for p in productos))
    return render_template('productos.html', productos=resultados, categorias=categorias)

@app.route('/editar/<int:producto_id>', methods=['POST'])
def editar(producto_id):
    productos = cargar_productos()
    for p in productos:
        if p['id'] == producto_id:
            p['nombre'] = request.form['nombre']
            p['precio'] = float(request.form['precio'])
            p['categoria'] = request.form['categoria']
            p['codigo'] = request.form.get('codigo', '')
            break
    guardar_productos(productos)
    return redirect('/')

@app.route('/eliminar/<int:producto_id>')
def eliminar(producto_id):
    productos = cargar_productos()
    productos = [p for p in productos if p['id'] != producto_id]
    guardar_productos(productos)
    return redirect('/')

@app.route('/pdf')
def generar_pdf():
    productos = cargar_productos()
    nombre_archivo = 'lista_productos.pdf'
    c = canvas.Canvas(nombre_archivo)
    c.setFont("Helvetica", 12)
    y = 800
    c.drawString(100, y, "Lista de Productos")
    y -= 20
    for p in productos:
        texto = f"{p['id']} - {p['nombre']} - ${p['precio']} - {p['categoria']} - Código: {p.get('codigo', '')}"
        c.drawString(100, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    return send_file(nombre_archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
