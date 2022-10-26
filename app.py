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

# Le indico al sistema de dónde leer la base de datos.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventas.db"
ventas.db.init_app(app)

@app.route("/")
def index():
    try:
       
        print("Renderizar index.html")
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})



@app.route("/venta")
def venta():
    try:
       
        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)

      
        data = ventas.report(limit=limit, offset=offset)

       
        print("Renderizar tabla.html")
        return render_template('tabla.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})



@app.route("/venta/<name>")
def ventas_historial(name):
    try:
       
        name = name.lower()
    
        print("Obtener gráfico de la persona", name)       
        time, numero_venta = ventas.laboratory(name)

        image_html = utils.graficar(time, numero_venta)
        return Response(image_html.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
      
        try:
           
            print("Renderizar registro.html")
            return render_template('registro.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
           
            nombre = str(request.form.get('name')).lower()
            apellido=str(request.form.get('last_name')).lower()
            cant_venta = str(request.form.get('numero_venta'))

            if(nombre is None or apellido is None or cant_venta.isdigit() is False):
                
                    return Response(status=400)
            time = datetime.now()

            print("Registrar Laboratorio", nombre, "apellido", apellido, "Cantidad Vendida", cant_venta)
            ventas.insert(time, nombre,apellido, int(cant_venta))

            
            return redirect(url_for('venta'))
        except:
            return jsonify({'trace': traceback.format_exc()})





@app.before_first_request
def before_first_request_func():
   
    ventas.db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Programa Python Iniciado')

    # activamos el server
    app.run(host="127.0.0.1", port=5000)