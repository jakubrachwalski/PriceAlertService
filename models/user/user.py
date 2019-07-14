__author__ = 'Jakub Rachwalski'

from typing import Dict
import uuid
# import re
from models.model import Model
from dataclasses import dataclass, field, asdict
from common.utils import Utils
import models.user.error as errors


@dataclass(eq=False)
class User(Model):

    collection: str = field(default="users", init=False)
    email: str
    passsord: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_by_email(cls, email: str) -> 'User':
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise errors.UserNotFound("User with this email has not been found!")

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise errors.InvalidEmail("The format of email is wrong")

        try:
            cls.get_by_email(email)
            raise errors.UserExists("This user is already registered!")
        except errors.UserNotFound:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    @classmethod
    def login_valid(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise errors.InvalidEmail("The format of email is wrong")

        user = cls.get_by_email(email)

        if not Utils.check_hashed_passwords(password, user.passsord):
            raise errors.WrongPassword("The password is incorrect!")

        return True
