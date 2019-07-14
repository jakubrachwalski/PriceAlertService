__author__ = 'Jakub Rachwalski'

from dataclasses import dataclass


@dataclass(eq=False)
class UserError(Exception):
    message: str


class UserNotFound(UserError):
    pass


class InvalidEmail(UserError):
    pass


class UserExists(UserError):
    pass


class WrongPassword(UserError):
    pass


class MailgunException(UserError):
    pass
