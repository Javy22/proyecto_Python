'''
Proyecto integrador Programador Python

Autor: Salinas Javier
Version: 1.0

Descripcion:
El programa permite el ingreso de vendedores por laboratorio para luego mostrar en gráficos las ventas 
realizadas por laboratorio.
'''

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Estadistica (db.Model):
    __tablename__ = "registro_venta"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    name = db.Column(db.String)
    apell = db.Column(db.String)
    value = db.Column(db.Integer)

    def __repr__(self):
        return f"Paciente {self.name} apellido {self.apell} ritmo cardíaco {self.value}"


def insert(time, name, last_name, numero_venta):
    # Crear un nuevo registro de ventas
    regis_venta = Estadistica(time=time, name=name,
                              apell=last_name, value=numero_venta)

    db.session.add(regis_venta)
    db.session.commit()


def report(limit=0, offset=0):
    json_result_list = []

    query = db.session.query(Estadistica).with_entities(
        Estadistica, db.func.count(Estadistica.name))

    # Agrupo por (laboratorio)

    query = query.group_by(Estadistica.name)

    # Ordeno por fecha para obtener el ultimo registro
    query = query.order_by(Estadistica.time)

    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    for result in query:
        regis_venta = result[0]
        cantidad = result[1]
        json_result = {}
        json_result['time'] = regis_venta.time.strftime("%Y-%m-%d %H:%M:%S.%f")
        json_result['name'] = regis_venta.name
        json_result['last_name'] = regis_venta.apell
        json_result['last_heartrate'] = regis_venta.value
        json_result['records'] = cantidad
        json_result_list.append(json_result)

    return json_result_list


def laboratory(name):
    # En esta funcion quiero mostrar las 100 primeras ventas ordenadas por fecha
    query = db.session.query(Estadistica).filter(
        Estadistica.name == name).order_by(Estadistica.time.desc())
    query = query.limit(100)
    query_results = query.all()

    if query_results is None or len(query_results) == 0:

        return [], []

    apell = [x.apell for x in reversed(query_results)]
    numero_venta = [x.value for x in reversed(query_results)]

    return apell, numero_venta


if __name__ == "__main__":
    print("Test del modulo ventas.py")
