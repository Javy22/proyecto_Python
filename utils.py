
'''
Proyecto integrador Programador Python
Archivo con utilidades para la app

Autor: Salinas Javier
Version: 1.0

Descripcion:
-----------------------------------------------------
Aquí podemos encontrar herramientas para utilizar en la aplicación
'''

import io
import base64

import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


def graficar(x, y):
    ''' 
     Gráfico para mostrar en html
    '''
   
    fig = plt.figure()
    fig.suptitle('Ventas por Visitador', fontsize=16, label='Laboratorio')
    ax = fig.add_subplot()

    ax.bar(x, y)
    ax.legend()
    ax.grid()
    ax.set_ylabel("Unidades")


    image_html = io.BytesIO()
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)  
    return image_html

    