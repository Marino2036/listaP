from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import sqlite3
import unicodedata

app = Flask(__name__)
DB_NAME = 'productos.db'

# ---------------------------- FUNCIONES DB ----------------------------

def conectar_db():
    return sqlite3.connect(DB_NAME)

def cargar_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, categoria, IFNULL(codigo, '') FROM productos")
    productos = [
        {"id": row[0], "nombre": row[1], "precio": row[2], "categoria": row[3], "codigo": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return productos

def agregar_producto(nombre, precio, categoria, codigo=""):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, categoria, codigo) VALUES (?, ?, ?, ?)",
                   (nombre, precio, categoria, codigo))
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()

def actualizar_precio(id_producto, nuevo_precio):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_producto))
    conn.commit()
    conn.close()

# ---------------------------- UTILIDAD ----------------------------

def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto.lower())
        if not unicodedata.combining(c)
    )

# ---------------------------- RUTAS ----------------------------

@app.route('/')
def lista_productos():
    consulta_original = request.args.get('q', '')
    consulta = normalizar(consulta_original)
    productos = cargar_productos()
    if consulta:
        resultados = [
            p for p in productos
            if consulta in normalizar(p['nombre']) or consulta in normalizar(p.get('codigo', ''))
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
    agregar_producto(nombre, precio, categoria, codigo)
    return redirect(url_for('lista_productos'))

@app.route('/eliminar/<int:id_producto>', methods=['POST'])
def eliminar(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for('lista_productos'))

@app.route('/actualizar/<int:id_producto>', methods=['POST'])
def actualizar(id_producto):
    nuevo_precio = float(request.form.get('precio'))
    actualizar_precio(id_producto, nuevo_precio)
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

# ---------------------------- INICIO ----------------------------

if __name__ == '__main__':
    app.run(debug=True)
