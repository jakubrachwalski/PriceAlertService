__author__ = 'Jakub Rachwalski'

import functools
from typing import Callable
from flask import url_for, redirect, session, flash, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_fucntion(*args, **kwargs):
        if not session.get("email"):
            flash('Page accessible only for logged in users', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_fucntion


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_fucntion(*args, **kwargs):
        if session.get("email") != current_app.config.get('ADMIN', ''):
            flash('Page accessible only for admin users', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_fucntion
