from comunidadesb import app, database
#from models import Usuario, Post


#isso nos da o "contexto" que o Flask está solicitando atualmente. Na prática não muda nada, apenas temos que colocar os códigos dentro desse "with"
with app.app_context():
    database.create_all()  #criando o banco de dados

    #CRIANDO USUÁRIOS
    # usuario = Usuario(username='Eduardinho', email='dudu@gmail.com', senha=123456)
    # usuario2 = Usuario(username='Nalivia', email='nali@gmail.com', senha=123456)


    # #SALVAR NA SESSÃO
    # database.session.add(usuario)
    # database.session.add(usuario2)


    # #SALVAR NO BANCO DE DADOS
    # database.session.commit()


    #FAZENDO UM BUSCA PELOS USUÁRIOS
    # meus_usuarios = Usuario.query.all()
    # print(meus_usuarios)
    # primeiro_usuario = meus_usuarios[0]
    # print(primeiro_usuario.username)


    #BUSCA PELO E-MAIL
    # usuario_teste = Usuario.query.filter_by(email='nali@gmail.com').first()
    # print(usuario_teste.username)


    #CRIANDO UM POST
    # meu_post = Post(id_usuario=1, titulo='Meu Primeiro Post', corpo='Teste Teste Testando')
    # database.session.add(meu_post)
    # database.session.commit()


    #CONSULTANDO O AUTOR DO POST
    # post = Post.query.first()
    # print(post.titulo)
    # print(post.autor.username)




    #RECRIANDO O BANCO DE DADOS
    #database.drop_all()
    #database.create_all()




