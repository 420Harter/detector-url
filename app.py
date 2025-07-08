from flask import Flask, request, render_template
import re
from urllib.parse import urlparse
import os  # <--- Añadido para Render

app = Flask(__name__)

def analizar_url(url):
    razones = []

    if "@" in url:
        razones.append("❌ Contiene '@', lo cual puede ser un intento de engaño.")

    ip_pattern = r"http[s]?://(?:\d{1,3}\.){3}\d{1,3}"
    if re.match(ip_pattern, url):
        razones.append("❌ Usa una dirección IP en lugar de un dominio.")

    if url.count("/") > 6:
        razones.append("⚠️ Tiene muchas barras '/', posible redirección sospechosa.")

    palabras_sospechosas = ["login", "update", "secure", "verify", "account", "bank"]
    if any(p in url.lower() for p in palabras_sospechosas):
        razones.append("⚠️ Contiene palabras sospechosas como 'login', 'verify', etc.")

    if not razones:
        razones.append("✅ No se detectaron señales sospechosas con las reglas simples.")

    return razones

def extraer_caracteristicas(url):
    parsed = urlparse(url)
    caracteristicas = {}

    caracteristicas["longitud_url"] = len(url)
    caracteristicas["contiene_ip"] = 1 if re.match(r"http[s]?://(?:\d{1,3}\.){3}\d{1,3}", url) else 0
    caracteristicas["cantidad_guiones"] = url.count("-")
    caracteristicas["cantidad_puntos"] = url.count(".")
    caracteristicas["contiene_arroba"] = 1 if "@" in url else 0
    caracteristicas["contiene_login"] = 1 if "login" in url.lower() else 0
    caracteristicas["cantidad_slash"] = url.count("/")
    caracteristicas["cantidad_parametros"] = url.count("?") + url.count("&")
    caracteristicas["tiene_https"] = 1 if parsed.scheme == "https" else 0

    return caracteristicas

@app.route("/", methods=["GET", "POST"])
def index():
    url = ""
    resultado = []
    caracteristicas = {}
    if request.method == "POST":
        url = request.form["url"]
        resultado = analizar_url(url)
        caracteristicas = extraer_caracteristicas(url)
    return render_template("index.html", url=url, resultado=resultado, caracteristicas=caracteristicas)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
