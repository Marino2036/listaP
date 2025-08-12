from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import psycopg2
import os
import unicodedata

app = Flask(__name__)

# ---------------------------- CONEXIÓN DB POSTGRES ----------------------------

def conectar_db():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

# ---------------------------- FUNCIONES DB ----------------------------

def cargar_productos(consulta=""):
    conn = conectar_db()
    cursor = conn.cursor()
    
    sql_query = "SELECT id, nombre, precio, categoria, COALESCE(codigo, '') FROM productos"
    
    if consulta:
        sql_query += """ WHERE unaccent(LOWER(nombre)) LIKE unaccent(LOWER(%s)) 
                          OR unaccent(LOWER(categoria)) LIKE unaccent(LOWER(%s)) 
                          OR unaccent(LOWER(codigo)) LIKE unaccent(LOWER(%s))"""
        search_term = f"%{consulta}%"
        cursor.execute(sql_query, (search_term, search_term, search_term))
    else:
        cursor.execute(sql_query)
        
    productos = [
        {"id": row[0], "nombre": row[1], "precio": row[2], "categoria": row[3], "codigo": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return productos

def agregar_producto(nombre, precio, categoria, codigo=""):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, categoria, codigo) VALUES (%s, %s, %s, %s)",
                   (nombre, precio, categoria, codigo))
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
    conn.commit()
    conn.close()

def actualizar_precio(id_producto, nuevo_precio):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET precio = %s WHERE id = %s", (nuevo_precio, id_producto))
    conn.commit()
    conn.close()

def actualizar_codigo(id_producto, nuevo_codigo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET codigo = %s WHERE id = %s", (nuevo_codigo, id_producto))
    conn.commit()
    conn.close()

# ---------------------------- UTILIDAD ----------------------------

def normalizar(texto):
    texto = texto.strip()
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto.lower())
        if not unicodedata.combining(c)
    )

# ---------------------------- RUTAS ----------------------------

@app.route('/')
def lista_productos():
    consulta_original = request.args.get('q', '')
    consulta = normalizar(consulta_original)
    
    productos = cargar_productos(consulta)
    
    return render_template('productos.html', productos=productos, consulta=consulta_original)

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

@app.route('/actualizar_codigo/<int:id_producto>', methods=['POST'])
def actualizar_codigo_ruta(id_producto):
    nuevo_codigo = request.form.get('codigo')
    actualizar_codigo(id_producto, nuevo_codigo)
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