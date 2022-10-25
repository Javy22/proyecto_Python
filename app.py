'''
Proyecto integrador Programador Python

Autor: Salinas Javier
Version: 1.0

Descripcion:
El programa permite el ingreso de vendedores por laboratorio para luego mostrar en gráficos las ventas 
realizadas por laboratorio.

'''

# Realizar HTTP POST con --> post.py

from datetime import datetime

import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for

import utils
import ventas

# Creamos el server Flask
app = Flask(__name__)

# Le indicamos al sistema de dónde leer la base de datos.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventas.db"
ventas.db.init_app(app)

# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:
        # Renderizamos el temaplate HTML index.html
        print("Renderizar index.html")
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/pulsaciones
@app.route("/venta")
def venta():
    try:
        # Obtener de la query string los valores de limit y offset
        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)

        # Obtener el reporte
        data = ventas.report(limit=limit, offset=offset)

        # Renderizar el temaplate HTML pulsaciones.html
        print("Renderizar tabla.html")
        return render_template('tabla.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/pulsaciones/<nombre>
@app.route("/venta/<name>")
def ventas_historial(name):
    try:
        # Obtener el nombre en minúscula
        name = name.lower()
        # Obtener el historial de la persona de la DB 
        print("Obtener gráfico de la persona", name)       
        time, heartrate = ventas.chart(name)

        # Transformar los datos en una imagen HTML con matplotlib
        image_html = utils.graficar(time, heartrate)
        return Response(image_html.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/registro
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        # Si entré por "GET" es porque acabo de cargar la página
        try:
            # Renderizar el temaplate HTML registro.html
            print("Renderizar registro.html")
            return render_template('registro.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            # Obtener del HTTP POST JSON el nombre (en minisculas) y los pulsos
            nombre = str(request.form.get('name')).lower()
            apellido=str(request.form.get('last_name')).lower()
            pulsos = str(request.form.get('heartrate'))

            if(nombre is None or apellido is None or pulsos is None or pulsos.isdigit() is False):
                # Datos ingresados incorrectos
                    return Response(status=400)
            time = datetime.now()

            print("Registrar persona", nombre, "con pulsaciones", pulsos)
            ventas.insert(time, nombre,apellido, int(pulsos))

            # Como respuesta al POST devolvemos la tabla de valores
            return redirect(url_for('venta'))
        except:
            return jsonify({'trace': traceback.format_exc()})




# Este método se ejecutará solo una vez
# la primera vez que ingresemos a un endpoint
@app.before_first_request
def before_first_request_func():
    # Crear aquí todas las bases de datos
    ventas.db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Inove@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)