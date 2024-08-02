#CRIAR OS FORMULÁRIOS DO SITE

from flask_wtf import FlaskForm       #Responsável pela criação dos formulários web
from flask_wtf.file import FileField, FileAllowed      #FileField = Campo de Arquivo, FileAllowed = É um validator. Ele determina quais extensões de arquivo serão permitidas o usuário colocar no Campo de Arquivo
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from comunidadesb. models import Usuario
from flask_login import current_user


#Significado dos Validadores:
# DataRequired = Verifica se o usuário preencheu o campo. Torna o campo obrigatório.
# Email = Verifica se o texto informado é realmente um e-mail.
# EqualTo = Verifica se um campo é igual ao outro. Será usadado para fazermos a verificação de senha.
# Length = Para determinar o tamanho da senha do usuário.
# ValidationError = Para quando der um erro, a mensagem ser exibida para o usuário.


# Como o FlasForm já possui todas as funções e características necessárias para criação de formulários, podemos definir apenas os campos desse formulário.
class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme sua Senha', validators=[DataRequired(), EqualTo("senha")])
    botao_submit_criarconta = SubmitField('Criar Conta')

# Essa função, por começar com a palavra "validate_", será rodada automaticamente com os validators. O responsável por rotar nossa função é esse cara: 'form_criarconta.validate_on_submit()'
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado.')



class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Manter Login')  #Boolean Field serve para deixarmos o login do usuário salvo
    botao_submit_login = SubmitField('Fazer Login')



class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    posicao_goleiro = BooleanField('Goleiro')
    posicao_fixo = BooleanField('Fixo')
    posicao_ala = BooleanField('Ala')
    posicao_pivo = BooleanField('Pivô')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail.')




class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Post', validators=[DataRequired()])
    botao_submit_criarpost = SubmitField('Publicar')






