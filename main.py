from flask import jsonify, request
from flask_migrate import Migrate

from app import app, db
from app.models import User, user_share_schema, users_share_schema
import datetime
import jwt

Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
    )

@app.route('/auth/register', methods=['POST'])
def register():

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    user = User(
        username,
        email,
        password
        )
    db.session.add(user)
    db.session.commit()

    result = user_share_schema.dump(
        User.query.filter_by(email=email).first()
    )

    return jsonify(result)

@app.route('/auth/login', methods=['POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first_or_404()

    if not user.verify_password(password):
        return jsonify({
            "error":"Suas credenciais estão erradas"
        }), 403
    
    payload = {
        "id":user.id,
        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    
    token = jwt.encode(payload, app.config['SECRET_KEY'])

    return jsonify({"token" : token.decode('utf-8')})
