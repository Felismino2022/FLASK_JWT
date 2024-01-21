from werkzeug.security import generate_password_hash, check_password_hash
from app import db, ma
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)


    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User : {self.username}>"

   #Para serialização(basicamente é pra termos um retorno json) 
class UserChema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')

#retorna um usuario
user_share_schema = UserChema()
#retorna varios usuarios
users_share_schema = UserChema(many=True)
