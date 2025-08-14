import calendar
import datetime
from flask import abort
from constants import JWT_SECRET, JWT_ALGORITHM
from service.user import UserService
import jwt

class AuthService:
    def __int__(self, user_service: UserService):
        self.user_service = user_service

    def generate_jwt(self, user_name, password, is_refresh=False):
        """Проверка наличия пользователя, пароля, создание токенов"""
        user = self.user_service.get_by_username(user_name)
        if user is None:
            return {"error": "Неверные учётные данные"}, abort(401)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                return {"error": "Неверный пароль"}, abort(401)

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201

    def refresh_token(self, refresh_token):
        """Получение рефреш токена"""
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get("username")

        return self.generate_jwt(username, None, is_refresh=True)




