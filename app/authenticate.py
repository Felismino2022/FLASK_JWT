from functools import wraps

import jwt
from app.models import User
from flask import request, jsonify, current_app


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = None
        print("filo")
        print(request.headers['authorization'])
        if 'authorization' in request.headers:
            token = request.headers['authorization']
            print("teste")

        if not token:
            return jsonify({"error":"Você não tem permissão para acessar essa rota"}), 403
        
        if not 'Bearer' in token:
            return jsonify({"error":"token invalido"}), 401
        
        try:
            token_pure = token.replace("Bearer", "").strip()
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(decoded['id'])
            
        except:
            return jsonify({"error":"O token é invalido"}), 403

        return func(current_user=current_user, *args, **kwargs)

    return wrapper