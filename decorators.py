from flask import abort, request
import jwt
from constants import JWT_ALGORITHM, JWT_SECRET


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in  request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("bearer ")[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        except Exception as e:
            print(e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("bearer ")[-1]
        role = None

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get("role")

        except Exception as e:
            print(e)
            abort(401)

        if role != "admin":
            abort(401 )

        return func(*args, **kwargs)

    return wrapper