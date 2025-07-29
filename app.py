from flask import Flask, render_template, request

app = Flask(__name__)

# Lista de productos de ejemplo
productos = [
    {"id": 1, "nombre": "boing 500ml", "precio": 10},
    {"id": 2, "nombre": "boing 250ml", "precio": 8},
    {"id": 3, "nombre": "Naranjada 600", "precio": 12},
    {"id": 4, "nombre": "Leche", "precio": 20},
    {"id": 5, "nombre": "Pan", "precio": 15}
]

@app.route('/')
def lista_productos():
    consulta = request.args.get('q', '').lower()
    resultados = [p for p in productos if consulta in p['nombre'].lower()] if consulta else productos
    return render_template('productos.html', productos=resultados, consulta=consulta)

if __name__ == '__main__':
    app.run(debug=True)
