import os
from functools import wraps

from flask import redirect, render_template, session


def is_admin_interface():
    return os.getenv("ADMIN", "false") == "true"


def is_development():
    return os.getenv("FLASK_ENV", "production") == "development"


def admin_interface(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not is_admin_interface():
            raise Exception("ADMIN not set when trying /admin")
        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "details" not in session:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def render_template_custom(app, template, **args):
    args["is_admin_interface"] = is_admin_interface()

    page_title = os.getenv("PAGE_TITLE", "GOV.UK")
    if is_development():
        page_title = "{} - {}".format(app.cf_space.upper(), page_title)
    args["title"] = page_title

    args["logged_in"] = "details" in session

    return render_template(template, **args)
