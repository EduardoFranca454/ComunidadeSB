#Todas as funções de páginas do site

from comunidadesb import app, database, bcrypt, login_manager
from flask import render_template, flash, redirect, request, url_for, abort
from comunidadesb.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from comunidadesb.models import Usuario, Post
from flask_login import login_user  #o responsável pelo login
from flask_login import logout_user, current_user, login_required
import secrets
import os  #para manusear os arquivos (tipos as fotos de perfil)
from PIL import Image


@app.route('/')  # O decorator é considerado uma função, e ele sempre virá antes de outra função. O decorator atribui uma nova funcionalidade para a função que está logo embaixo dele.
def homepage():
    posts = Post.query.order_by(Post.id.desc()) #Post.id.desc() = utilizado para mudarmos o sentido que os posts serão mostrados na homepage. Dessa forma, os posts mais recentes irão aparecer primeiro
    return render_template("homepage.html", posts=posts)


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])  #Tivemos que habilitar o método 'POST' na nossa página. Como padrão, nossas páginas são sempre criadas apenas com o 'GET', mas por se tratar de uma página que possui formulários, tivemos que habilitar o 'POST'
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form: #Ta verificando se o formulário foi validado e se o botão que foi clicado foi o "botao_submit_login"
        usuario = Usuario.query.filter_by(email=form_criarconta.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # fazer login
            login_user(usuario, remember=form_login.lembrar_dados.data)  #'remember' = é o que determina se as informações de login ficarão salvas ou não. E como demos a possibilidade do usuário escolher se ele quer deixar o login salvo ou não, vamos usar a resposta dele "form_login.lembrar_dados.data" para definir.

            # exibir a mensagem de login bem sucedido
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')  #form_login.email.data = é o valor que o usuário preencheu no campo "e-mail" do formulário de login

            # redirecionamento automático e inteligente: redireciona de acordo com a página que o usuário clicou.
            parametro_next = request.args.get('next')  #pegando o parâmetro next
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        # criar o usuário
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)

        # adicionar sessão
        database.session.add(usuario)

        # salvar
        database.session.commit()

        # exibir a mensagem de criação de conta bem sucedida
        flash(f'Conta criada com sucesso no e-mail: {form_criarconta.email.data}', 'alert-success')  # "alert-sucess" =  é a categoria do nosso alerta

        # redirecionar o usuário para a homepage
        return redirect(url_for('homepage'))
    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('homepage'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("perfil.html", foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit():
        post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso!', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template("criarpost.html", form_criarpost=form_criarpost)


def salvar_imagem(imagem):
    # Adicionar um código aleatório junto do nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)   #separa o nome (default) e a extensão (jpg) do arquivo
    nome_arquivo = nome + codigo + extensao  #juntando tudo para termos o nome do arquivo
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)  #caminho onde as imagens serão salvas

    # Reduzir o tamanho da imagem
    tamanho = (500, 500)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # Salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


def atualizar_cursos(form):
    lista_posicoes = []
    for campo in form:
        if 'posicao_' in campo.name:
            if campo.data:
                lista_posicoes.append(campo.label.text)
    return ' / '.join(lista_posicoes)


@app.route('/perfil/editar', methods=['GET', 'POST'])  #Toda página que tem um formulário deve ter, obrigatoriamente, essa adição do método POST
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()
    # Editando as CARACTERÍSTICAS do usuário
    if form_editar_perfil.validate_on_submit():
        # Mudando e-mail
        current_user.email = form_editar_perfil.email.data
        #Mudando nome de usuário
        current_user.username = form_editar_perfil.username.data
        #Alterando a foto de perfil caso o usuário tenha feito a mudança
        if form_editar_perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        # Determinando a posição que o usuário joga
        current_user.posicoes = atualizar_cursos(form_editar_perfil)

        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))

    elif request.method == 'GET': #faz com que o formulário de edição de perfil seja aberto já preenchido
        form_editar_perfil.email.data = current_user.email
        form_editar_perfil.username.data = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("editarperfil.html", foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)



@app.route('/post/<post_id>', methods=['GET', 'POST'])  #<post_id> = uma variável no nosso link
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado!', 'alert-success')
            return redirect(url_for('homepage'))

    else:
        form = None
    return render_template('post.html', post=post, form=form)



@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído!', 'alert-danger')
        return redirect(url_for('homepage'))
    else:
        abort(403)  #Esse 403 significa um erro de permissão, ou seja, o usuário será notificado caso ele tente entrar onde não pode
