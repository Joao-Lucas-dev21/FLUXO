from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for

# Entrar na pasta cd Meu_Projeto
# dps python Fluxo.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testeuser:39050669@localhost:3306/fluxo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column('id_Usuario', db.Integer, primary_key=True)
    nome = db.Column('Usu_nome', db.String(256))
    email = db.Column('Usu_email', db.String(256))
    senha = db.Column('Usu_senha', db.String(256))
    endereco = db.Column('Usu_endereco', db.String(256))

    def __init__(self, nome, email, senha, endereco):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco


class Anuncio(db.Model):
    id = db.Column('id_Anuncio', db.Integer, primary_key=True)
    nome_Do_Anuncio = db.Column('Anun_nome_anuncio', db.String(256))
    valor_Anuncio = db.Column('Anun_valor', db.Double)
    quantidade_Anuncio = db.Column('Anun_quantidade', db.Double)
    descricao_Anuncio = db.Column('Anun_descricao_Anuncio', db.String(256))

    def __init__(self, nome_Anuncio, valor_Anuncio, quantidade_Anuncio ,descricao_Anuncio):
        self.nome_Do_Anuncio = nome_Anuncio
        self.valor_Anuncio = valor_Anuncio
        self.quantidade_Anuncio = quantidade_Anuncio
        self.descricao_Anuncio = descricao_Anuncio


class Categoria(db.Model):
    id = db.Column('id_Tema', db.Integer, primary_key=True)
    tema = db.Column('tema', db.String(100))

    def __init__(self, tema):
        self.tema = tema

##class Anuncio_Fav(db.Model):

##    def __init__(self):
  ##      super().__init__()

##class Pergunta_Resposta(db.Model):
##    pergunta_Anuncio = db.Column('pergunta', db.String(256))
##    resposta_Anuncio = db.Column('resposta', db.String(256))

##    def __init__(self, pergunta_Anuncio, resposta_Anuncio):
  ##      self.pergunta_Anuncio = pergunta_Anuncio
##        self.resposta_Anuncio = resposta_Anuncio

##class Compra(db.Model):


##class Relatorio_Vendas(db.Model):


##class Relatorio_Compra(db.Model):
    

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastrar/usuario/")
def user_Cad():
    return render_template("user_Cad.html", usuarios = Usuario.query.all())


@app.route("/cadastro/novo/", methods=["POST"])
def cadastro():
    usuario = Usuario(request.form.get('nome'), request.form.get('email'), request.form.get('senha'), request.form.get('endereco'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('user_Cad'))


@app.route("/cadastro/detalhes/<int:id>")
def mostrarDetalhes(id):
    usuario = Usuario.query.get(id)
    return usuario.nome


@app.route("/deletar/usuario/<int:id>")
def deletarUsuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('user_Cad'))

@app.route("/cadastro/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizarUsuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('endereco')
        usuario.endereco = request.form.get('endereco')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('user_Cad'))
    return render_template('atualizar_Cadastro.html', usuario = usuario)

@app.route("/anuncio/")
def anuncio():
    return render_template("anuncio.html", anuncios = Anuncio.query.all())

@app.route("/detalhes/anuncio/<int:id>")
def mostrarAnuncio(id):
    anuncio = Anuncio.query.get(id)
    return anuncio.nome_Do_Anuncio


@app.route("/criar/anuncio", methods=['POST'])
def criarAnuncio():
    anuncio = Anuncio(request.form.get('nome_anuncio'), request.form.get('valor_Anuncio'), request.form.get('quantidade'), request.form.get('descricao_Anuncio'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/deletar/anuncio/<int:id>")
def deletarAnuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/atualizar/anuncio/<int:id>", methods=['GET', 'POST'])
def atualizarAnuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome_Do_Anuncio = request.form.get('nome_anuncio')
        anuncio.valor_Anuncio = request.form.get('valor_Anuncio')
        anuncio.quantidade_Anuncio = request.form.get('quantidade')
        anuncio.descricao_Anuncio = request.form.get('descricao_Anuncio')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))
    return render_template('atualizar_Anuncio.html', anuncio = anuncio)


@app.route("/anuncio/categoria/")
def categoria():
    return render_template("categoria.html", categorias = Categoria.query.all())

@app.route("/detalhes/categoria/<int:id>")
def mostrarCategoria(id):
    categoria = Categoria.query.get(id)
    return categoria.tema

@app.route("/criar/categoria", methods=['POST'])
def criarCategoria():
    categoria = Categoria(request.form.get('nome_Categoria'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/deletar/categoria/<int:id>")
def deletarCategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/atualizar/categoria/<int:id>", methods=['GET', 'POST'])
def atualizarCategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.tema = request.form.get('nome_Categoria')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('atualizar_Categoria.html', categoria = categoria)



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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    print("Tabela Criada com Sucesso!")
