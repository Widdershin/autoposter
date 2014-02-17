# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user
from autoposter.user.models import Post
from .forms import NewPostForm

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/posts")
@login_required
def posts():
    return render_template("users/posts.html", posts=current_user.posts)


@blueprint.route("/posts/add", methods=('GET', 'POST'))
@login_required
def add_post():
    form = NewPostForm()

    if form.validate_on_submit():
        new_post = Post()
        form.populate_obj(new_post)
        current_user.posts.append(new_post)

        new_post.save()
        current_user.save()

        return redirect(url_for('user.posts'))

    return render_template("users/newpost.html", form=form)


@blueprint.route("/posts/edit/<id>", methods=('GET', 'POST'))
@login_required
def edit_post(id):
    post = Post.query.get(id)

    if post not in current_user.posts:
        return abort(401)

    form = NewPostForm(obj=post)

    if form.validate_on_submit():

        form.populate_obj(post)

        post.save()

        flash("{} saved successfully!".format(post.title))

        return redirect(url_for('user.posts'))

    return render_template("users/newpost.html", form=form)
