from flask import render_template, redirect, url_for, flash, request, abort
from lipsart import app, database, bcrypt
from lipsart.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarPost
from lipsart.models import Usuario, Post
# 30. Login dos Usuários (login_user)
# 31. Personalizando o Site para Usuários Logados (logout_user e current_user)
# 32. Bloquear Página para Usuários Visitantes (login_required)
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    # 45. Ajeitando a HomePage - Feed de Posts
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


# 11. Puxando Informações de Forma Dinâmica do Python para o Site
@app.route('/usuarios')
@login_required
def usuarios():
    # 43. Preenchendo Lista de Usuários do Banco de Dados
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


# 14. Criando Página de Login e Criar Conta
# 19. Liberando Método Post das Páginas (acrescentei o method POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 17. Adicionando Formulários no HTML
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    # 20. csrf token e Mensagem de Sucesso nos Formulários
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # 30. Login dos Usuários
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login efetuado com sucesso para o e-mail {form_login.email.data}', 'alert-success')
            # 33. Redirecionamento Automático Inteligente
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # 27. Criando usuário no banco de dados com nosso formulário
        # 28. Criptografando a Senha do Usuário
        senha_criptografada = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario_criado = Usuario(
            usuario=form_criarconta.usuario.data,
            email=form_criarconta.email.data,
            senha=senha_criptografada
        )
        database.session.add(usuario_criado)
        database.session.commit()
        flash(f'Conta criada com sucesso para o e-mail {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
# 32. Bloquear Página para Usuários Visitantes
@login_required
def sair():
    logout_user()
    flash('Logout Efetuado com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
# 32. Bloquear Página para Usuários Visitantes
@login_required
def perfil():
    # 35. Carregando a imagem padrão de Perfil
    foto = url_for('static', filename=f'fotos_perfil/{current_user.foto}')
    # print(foto)
    return render_template('perfil.html', foto=foto)


# 44. Permitir a Criação de Post
@app.route('/criar/post', methods=['GET', 'POST'])
# 32. Bloquear Página para Usuários Visitantes
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


# 39. Salvar e Compactar Imagem no Banco de Dados
def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


# 41. Editando o Campo Cursos do Banco de Dados
def atualizar_cursos(form):
    lista_curso = []
    for campo in form:
        if 'curso_' in campo.name and campo.data:
            lista_curso.append(campo.label.text)
    # Ajuste que precisei fazer, pois quando não informado o Curso, não ficava o valor default
    if not lista_curso:
        return 'Não Informado'
    return ';'.join(lista_curso)


# 36. Edição do Perfil
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    foto = url_for('static', filename=f'fotos_perfil/{current_user.foto}')
    form = FormEditarPerfil()
    # 37. Funcionalidade do Formulário de Editar Perfil
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.usuario = form.usuario.data
        # 39. Salvar e Compactar Imagem no Banco de Dados
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto = nome_imagem
        # 41. Editando o Campo Cursos do Banco de Dados
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.usuario.data = current_user.usuario
    return render_template('editarperfil.html', foto=foto, form=form)


# 47. Uma Página para cada Post
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def visualizar_post(post_id):
    post = Post.query.get(post_id)
    # 48. Criando Edição do Post
    if current_user == post.autor:
        form = FormEditarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


# 50. Excluir Post
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post deletado', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
