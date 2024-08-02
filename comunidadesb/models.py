#Arquivo responsável pelo banco de dados

from comunidadesb import database, login_manager
from datetime import datetime
from flask_login import UserMixin  #UserMixin é um parâmetro que vamos passar para nossa classe, que irá atribuir a ela todas as características que o Login Manager precisa



# O Login Manager necessita de uma função que encontre o usuário
# E dessa forma, estamos passando para o Login Manager a função que irá fazer essa ação
@login_manager.user_loader
def load_usuario(id_usuario): #id_usuario = primary key
    return Usuario.query.get(int(id_usuario))



class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
                                #'Post' = Nome da outra tabela que faz parte do relationship
                                #'backref' = Nome do usuário que criou determinado post. Para descobrir o nome do usuário, vamos usar a palavra 'autor' como sendo um método, por exemplo: post.autor
                                #lazy=True = serve para otimizar a resposta do banco de dados.
    posicoes = database.Column(database.String, nullable=False, default='Não Informado')

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)   #.Text = campo de texto. É usado para determinar campos que são maiores do que os de string convencionais.
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
                                #database.ForeignKey('usuario.id') = serve para pegarmos a coluna ID da tabela Usuario (tem que ser escrito em letra minúscula) e trazer para a tabela Post

