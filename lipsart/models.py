# 23. Criação das Tabelas do Banco de Dados
from lipsart import database, login_manager
# 30. Login dos Usuários
from datetime import datetime, timezone
# 30. Login dos Usuários
from flask_login import UserMixin


# 30. Login dos Usuários
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))
    # aqui usamos o método .get ao invés do filter porque estamos resgatando os dados a partir de uma primary key da \
    # tabela. O método .get usa a chave primaria.


# 30. Login dos Usuários (inclusao do UserMixin como herança da classe)
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    usuario = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto = database.Column(database.String, default='default.jpg')
    # 24. Relacionamento entre Posts e Usuários
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    # 51. Método de Contagem de Posts
    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.String, nullable=False)
    data = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    # 24. Relacionamento entre Posts e Usuários
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

