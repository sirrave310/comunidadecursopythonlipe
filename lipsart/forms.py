# 15. Formulários do Site
from flask_wtf import FlaskForm
# 38. Campo de Edição de Foto de Perfil
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, SubmitField, PasswordField, EmailField, BooleanField, TextAreaField
)
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
# 29. Criando validação Personalizada - Usuários Únicos
from lipsart.models import Usuario
# 37. Funcionalidade do Formulário de Editar Perfil
from flask_login import current_user


class FormCriarConta(FlaskForm):
    usuario = StringField('Nome de Usuário', validators=[DataRequired()])
    email = EmailField(
        'E-mail',
        validators=[
            DataRequired(),
            Email(message='Endereço de e-mail inválido.')
        ]  # 21. Validações dos Campos dos Formulários
    )
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField(
        'Confirme a Senha',
        validators=[
            DataRequired(),
            EqualTo('senha', message='O campo deve ser igual à senha.')
        ]  # 21. Validações dos Campos dos Formulários
    )
    botao_submit_criarconta = SubmitField('Criar Conta')

    # 29. Criando validação Personalizada - Usuários Únicos
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Esse e-mail já está cadastrado. Tente outro ou faça login.')


class FormLogin(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email(message='Endereço de e-mail inválido.')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')  # 18. Aplicando Bootstrap
    botao_submit_login = SubmitField('Entrar')


# 36. Edição do Perfil
class FormEditarPerfil(FlaskForm):
    usuario = StringField('Nome de Usuário', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email(message='Endereço de e-mail inválido.')])
    botao_submit_confirmaredicao = SubmitField('Confirmar Edição')
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])

    # 40. Revisando o Site e Adicionando Cursos no Form do Perfil
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('Power BI')
    curso_python = BooleanField('Python')
    curso_ppt = BooleanField('Power Point')
    curso_sql = BooleanField('SQL')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro.')


# 44. Permitir a Criação de Post
class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')


class FormEditarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Atualizar Post')