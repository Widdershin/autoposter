# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user
from autoposter.user.models import User

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/posts")
@login_required
def posts():
    return render_template("users/posts.html", posts=current_user.posts)
