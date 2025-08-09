from flask import Flask
from flask import make_response
from markupsafe import escape   
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro/")
def user_Cad():
    return render_template("user_Cad.html")

@app.route("/cadastrado_Usuario", methods=["POST"])
def cadastaro():
    return request.form

@app.route("/anuncio/")
def anuncio():
    return render_template("anuncio.html")

@app.route("/anuncio/categoria/")
def categoria():
    return render_template("categoria.html")

@app.route("/anuncio/pergunta")
def pergunta():
    return render_template("pergunta.html")

@app.route("/compras")
def compra():
    return render_template("compra.html")

@app.route("/anuncio_fav")
def ads_fav():
    return render_template("anuncio_fav.html")  

@app.route("/relatorio_venda")
def relatorio_venda():
    return render_template("relatorio_venda.html")

@app.route("/relatorio_compra")
def relatorio_compra():
    return render_template("relatorio_compra.html")