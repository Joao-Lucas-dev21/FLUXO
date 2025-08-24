from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import hashlib
from flask import Flask, send_from_directory
from werkzeug.security import check_password_hash

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testeuser:39050669@localhost:3306/fluxo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Jo4o:39050669Jo@Jo4o.mysql.pythonanywhere-services.com:3306/Jo4o$mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = '39050669'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('id_Usuario', db.Integer, primary_key=True)
    nome = db.Column('Usu_nome', db.String(256))
    email = db.Column('Usu_email', db.String(256))
    senha = db.Column('Usu_senha', db.String(256))
    endereco = db.Column('Usu_endereco', db.String(256))

    favoritos = db.relationship(
        "Anuncio",
        secondary="anuncio_fav",
        backref="usuarios_favoritaram"
    )

    def __init__(self, nome, email, senha, endereco):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('id_Anuncio', db.Integer, primary_key=True)
    nome_Do_Anuncio = db.Column('Anun_nome_anuncio', db.String(256))
    valor_Anuncio = db.Column('Anun_valor', db.Double)
    quantidade_Anuncio = db.Column('Anun_quantidade', db.Double)
    descricao_Anuncio = db.Column('Anun_descricao_Anuncio', db.String(256))
    id_categoria = db.Column(db.Integer, db.ForeignKey(
        'categoria.id_Tema'))  # nova coluna
    categoria = db.relationship("Categoria", backref="anuncios")

    def __init__(self, nome_Anuncio, valor_Anuncio, quantidade_Anuncio, descricao_Anuncio, id_categoria):
        self.nome_Do_Anuncio = nome_Anuncio
        self.valor_Anuncio = valor_Anuncio
        self.quantidade_Anuncio = quantidade_Anuncio
        self.descricao_Anuncio = descricao_Anuncio
        self.descricao_Anuncio = descricao_Anuncio
        self.id_categoria = id_categoria


class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('id_Tema', db.Integer, primary_key=True)
    tema = db.Column('tema', db.String(100))

    def __init__(self, tema):
        self.tema = tema


class Anuncio_Fav(db.Model):
    __tablename__ = "anuncio_fav"
    id = db.Column(db.Integer, primary_key=True)
    id_Usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_Usuario"))
    id_Anuncio = db.Column(db.Integer, db.ForeignKey("anuncio.id_Anuncio"))

    def __init__(self, id_Usuario, id_Anuncio):
        self.id_Usuario = id_Usuario
        self.id_Anuncio = id_Anuncio



@app.route('/logo')
def logo():
    return send_from_directory('.', 'Logo-Fluxo.jpeg')


@app.errorhandler(404)
def paginaNaoEncontrada(error):
    return render_template('error_Page.html')


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)


@app.route("/")
@login_required
def index():
    return render_template("index.html", anuncios=Anuncio.query.all())


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = hashlib.sha512(
            str(request.form.get('senha')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(email=email, senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/cadastrar/usuario/", methods=['GET', 'POST'])
def user_Cad():
    return render_template("user_Cad.html", usuarios=Usuario.query.all())


@app.route("/cadastro/novo/", methods=['GET', 'POST'])
def cadastro():
    hash = hashlib.sha512(
        str(request.form.get('senha')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('nome'), request.form.get(
        'email'), hash, request.form.get('endereco'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('login'))


@app.route("/cadastro/detalhes/<int:id>")
@login_required
def mostrarDetalhes(id):
    usuario = Usuario.query.get(id)
    return usuario.nome


@app.route("/deletar/usuario/<int:id>")
@login_required
def deletarUsuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('user_Cad'))


@app.route("/cadastro/atualizar/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizarUsuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.senha = hashlib.sha512(
            str(request.form.get('senha')).encode("utf-8")).hexdigest()
        usuario.endereco = request.form.get('endereco')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('user_Cad'))
    return render_template('atualizar_Cadastro.html', usuario=usuario)


@app.route("/anuncio/")
def anuncio():
    return render_template("anuncio.html", anuncios=Anuncio.query.all())


@app.route("/detalhes/anuncio/<int:id_Anuncio>")
@login_required
def mostrarAnuncio(id_Anuncio):
    anuncio = Anuncio.query.get(id_Anuncio)
    usuario = current_user
    return render_template("anuncioDetalhes.html", anuncio=anuncio, usuario=usuario)


@app.route("/criar/anuncio", methods=['POST'])
@login_required
def criarAnuncio():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        nome = request.form.get('nome_anuncio')
        valor = request.form.get('valor_Anuncio')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao_Anuncio')
        id_categoria = request.form.get('categoria')

        anuncio = Anuncio(nome, valor, quantidade, descricao, id_categoria)
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))
    return redirect(url_for('anuncio', categorias=categorias))


@app.route("/deletar/anuncio/<int:id>")
@login_required
def deletarAnuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/atualizar/anuncio/<int:id>", methods=['GET', 'POST'])
@login_required
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
    return render_template('atualizar_Anuncio.html', anuncio=anuncio)


@app.route("/anuncio/categoria/")
def categoria():
    return render_template("categoria.html", categorias=Categoria.query.all())


@app.route("/detalhes/categoria/<int:id>")
@login_required
def mostrarCategoria(id):
    categoria = Categoria.query.get(id)
    return categoria.tema


@app.route("/criar/categoria", methods=['POST'])
@login_required
def criarCategoria():
    categoria = Categoria(request.form.get('nome_Categoria'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/deletar/categoria/<int:id>")
@login_required
def deletarCategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/atualizar/categoria/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizarCategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.tema = request.form.get('nome_Categoria')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('atualizar_Categoria.html', categorias=categoria)


@app.route("/anuncio/pergunta")
def pergunta():
    return render_template("pergunta.html")


@app.route("/compras")
def compra():
    return render_template("compra.html")


@app.route("/favorito/anuncio/<int:id_Anuncio>")
@login_required
def favoritar(id_Anuncio):
    usuario = current_user
    anuncio = Anuncio.query.get_or_404(id_Anuncio)

    if anuncio not in usuario.favoritos:
        usuario.favoritos.append(anuncio)
        db.session.commit()

    return redirect(url_for('mostrarAnuncio', id_Anuncio=id_Anuncio))


@app.route("/mostrar/favoritos")
@login_required
def mostrarFavoritos():
    favoritos = current_user.favoritos
    return render_template("anuncio_fav.html", favoritos=favoritos)


@app.route("/anuncio_fav/remover/<int:id_Anuncio>")
@login_required
def removerFav(id_Anuncio):
    usuario = current_user
    anuncio = Anuncio.query.get_or_404(id_Anuncio)

    if anuncio in usuario.favoritos:
        usuario.favoritos.remove(anuncio)
        db.session.commit()

    return redirect(url_for('mostrarFavoritos'))


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

