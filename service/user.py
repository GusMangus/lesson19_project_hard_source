import hashlib
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, algo


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        return self.dao.update(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password):
        return hashlib.pbkdf2_hmac(
            algo,
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def compare_passwords(self, password_hash, other_password):
        second_hash = hashlib.pbkdf2_hmac(algo, other_password.encode("utf-8"),
                                          PWD_HASH_SALT, PWD_HASH_ITERATIONS).decode("utf-8", "ignore")
        return hmac.compare_digest(password_hash.encode("utf-8", "ignore"), second_hash.encode("utf-8", "ignore"))


