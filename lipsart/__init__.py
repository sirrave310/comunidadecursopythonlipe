# 26. Reestruturando o Projeto (migrei tudo para esse arquivo, para reestruturação do projeto)

# 13. Padronizando Links do Site (importado o url_for)
from flask import Flask
# 26. Reestruturando o Projeto (não precisa mais desse import aqui)
# 17. Adicionando Formulários no HTML
# from forms import FormLogin, FormCriarConta
# 22. Banco de Dados para o Site
from flask_sqlalchemy import SQLAlchemy
# 28. Criptografando a Senha do Usuário
from flask_bcrypt import Bcrypt
# 30. Login dos Usuários
from flask_login import LoginManager
# 54. Colocando o site no ar - Railway + GitHub
import os
# 54. Colocando o site no ar - Railway + GitHub
import sqlalchemy


app = Flask(__name__)

# 16. Segurança dos Formulários no Site
app.config['SECRET_KEY'] = '301d692f8fb0ed1c9e8b35699fb37acf'

# 22. Banco de Dados para o Site
# 54. Colocando o site no ar - Railway + GitHub
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
database = SQLAlchemy(app)
# 30. Login dos Usuários
login_manager = LoginManager(app)
# 32. Bloquear Página para Usuários Visitantes
login_manager.login_view = 'login'
login_manager.login_message = 'É necessário se logar antes para acessar essa página.'
login_manager.login_message_category = 'alert-info'

# 28. Criptografando a Senha do Usuário
bcrypt = Bcrypt(app)

# 54. Colocando o site no ar - Railway + GitHub
from lipsart import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Base de Dados criada')
else:
    print('Base de dados já existente')


from lipsart import routes

