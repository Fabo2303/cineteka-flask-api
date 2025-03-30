from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapers.p.moviesscraper import (
    obtener_peliculas as p_obtener_peliculas,
)
from scrapers.p.schedulescraper import (
    obtener_horarios as p_obtener_horarios,
)
from scrapers.m.moviesscraper import (
    obtener_peliculas as m_obtener_peliculas,
)
from scrapers.m.schedulescraper import (
    obtener_horarios as m_obtener_horarios,
)

from dotenv import load_dotenv
import os

NOMBRE1 = os.getenv("P")
NOMBRE2 = os.getenv("M")

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

peliculas = []
horarios = []
last_consulted = ""


@app.route("/peliculas", methods=["GET"])
def scrap():
    global peliculas

    if len(peliculas) == 0:
        peliculas_p = p_obtener_peliculas()
        peliculas_m = m_obtener_peliculas()
        peliculas = peliculas_p + peliculas_m

    return jsonify({"message": "Scraping completado.", "peliculas": peliculas})


@app.route("/horarios", methods=["GET"])
def get_horarios():
    global horarios
    global last_consulted
    type = request.args.get("type")
    url = request.args.get("url")
    if len(horarios) == 0 or last_consulted != url:
        if type == NOMBRE2:
            horarios = p_obtener_horarios(url)
        elif type == NOMBRE1:
            horarios = m_obtener_horarios(url)
        last_consulted = url

    return jsonify({"message": "Scraping completado.", "horarios": horarios})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
