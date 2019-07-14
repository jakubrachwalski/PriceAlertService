__author__ = 'Jakub Rachwalski'

import re
from passlib.hash import pbkdf2_sha512

class Utils:

    @staticmethod
    def email_is_valid(email: str) -> bool:
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        return True if EMAIL_REGEX.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_hashed_passwords(password: str, hashed: str) -> bool:
        return pbkdf2_sha512.verify(password, hashed)
