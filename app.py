# app.py

from flask import Flask, jsonify
from flask_cors import CORS
import math
import random

app = Flask(__name__)
CORS(app)

# Coordenadas de las ciudades
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

# Función para calcular distancia entre dos coordenadas
def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# Evaluar la distancia total de una ruta
def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i+1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

# Algoritmo Hill Climbing
def hill_climbing():
    ruta = list(coord.keys())
    random.shuffle(ruta)
    mejora = True
    while mejora:
        mejora = False
        dist_actual = evalua_ruta(ruta)
        for i in range(len(ruta)):
            if mejora:
                break
            for j in range(len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist = evalua_ruta(ruta_tmp)
                    if dist < dist_actual:
                        mejora = True
                        ruta = ruta_tmp[:]
                        break
    return ruta

# Ruta API para resolver el TSP
@app.route('/tsp', methods=['GET'])
def resolver_tsp():
    ruta = hill_climbing()
    distancia_total = evalua_ruta(ruta)
    coordenadas = [coord[ciudad] for ciudad in ruta]
    return jsonify({
        'ruta': ruta,
        'coordenadas': coordenadas,
        'distancia_total': distancia_total
    })

# Levantar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
