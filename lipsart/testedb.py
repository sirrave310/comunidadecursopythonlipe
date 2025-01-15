from lipsart import app
from lipsart.models import Usuario, Post

with app.app_context():
    # usuario = Usuario.query.filter_by(usuario='Apolo-rook').first()
    # print(usuario.cursos)
    post = Post.query.all()
    print(post[3].titulo, post[3].corpo, sep='\n')
    # print(usuario.email)
    # print(usuario.senha)

    # database.drop_all()
    # database.create_all()