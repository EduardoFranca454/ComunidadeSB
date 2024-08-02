#Configuração principal do Site

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager   #gerenciador de login
import os

#Criação do APP:
app = Flask(__name__)

#Configurações do APP:
app.config['SECRET_KEY'] = '070c393726f45336b9b86d1c62dcffb6'

#Isso quer dizer que: Se o nosso código estiver rodando em um servidor que está online, o nosso banco de dados será esse "os.getenv("DATABASE_URL")", caso contrário, caso o código esteja rodando no servidor local, o nosso banco de dados será aquele que já estávamos usando 'sqlite:///comunidade.db'
#Ação necessária para darmos deploy no site
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'  #graças a essas 3 barras, o banco de dados será criado no mesmo lugar que nosso arquivo "main" está.

# Banco de Dados:
database = SQLAlchemy(app)  #criação do banco de dados

# Criptografia de Senha:
bcrypt = Bcrypt(app)

# Configurações de Login:
login_manager = LoginManager(app)
login_manager.login_view = 'login'  #É o responsável por fazer o redirecionamento do usuário para o página de login, quando o mesmo não estiver logado.
                                    #Ou seja, quando o usuário, sem estar logado, tentar acessar alguma página que determinamos como "@login_required", ele será informado que é uma página bloqueada para quem não está logado e será redirecionado para fazer login.

login_manager.login_message = 'Por favor, faça o Login para acessar essa página.'  #mensagem que irá aparecer quando o usuário tentar acessar uma página bloqueada e ele não estiver logado
login_manager.login_message_category = 'alert-info'  #faz com que a mensagem seja exibida de uma forma mais bonitinha.



#Importação necessária para carregarmos as páginas do Site.
from comunidadesb import routes
