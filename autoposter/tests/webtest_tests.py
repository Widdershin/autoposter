## -*- coding: utf-8 -*-
'''Functional tests using WebTest.

See: http://webtest.readthedocs.org/
'''
from flask import url_for
from flask.ext.webtest import TestApp
from nose.tools import *  # PEP8 asserts

from ..user.models import User
from .base import DbTestCase, LoggedInUserCase
from .factories import UserFactory, PostFactory


class TestLoggingIn(DbTestCase):

    def setUp(self):
        self.w = TestApp(self.app)
        self.user = UserFactory(password="myprecious")
        self.user.save()

    def test_can_log_in(self):
        # Goes to homepage
        res = self.w.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = self.user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert_equal(res.status_code, 200)

    def _login(self, username, password):
        res = self.w.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = username
        form['password'] = password
        # Submits
        res = form.submit().follow()
        return res

    def test_sees_alert_on_log_out(self):
        res = self._login(self.user.username, 'myprecious')
        res = self.w.get(url_for('public.logout')).follow()
        # sees alert
        assert_in('You are logged out.', res)

    def test_sees_error_message_if_password_is_incorrect(self):
        # Goes to homepage
        res = self.w.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = self.user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert_in("Invalid password", res)

    def test_sees_error_message_if_username_doesnt_exist(self):
        # Goes to homepage
        res = self.w.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert_in("Unknown user", res)


class TestRegistering(DbTestCase):

    def setUp(self):
        self.w = TestApp(self.app)

    def test_can_register(self):
        # Goes to homepage
        res = self.w.get("/")
        # Clicks Create Account button
        res = res.click("Create account")
        # Fills out the form
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert_equal(res.status_code, 200)
        # A new user was created
        assert_equal(len(User.query.all()), 1)

    def test_sees_error_message_if_passwords_dont_match(self):
        # Goes to registration page
        res = self.w.get(url_for("public.register"))
        # Fills out form, but passwords don't match
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert_in("Passwords must match", res)

    def test_sees_error_message_if_user_already_registered(self):
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = self.w.get(url_for("public.register"))
        # Fills out form, but username is already registered
        form = res.forms["registerForm"]
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert_in("Username already registered", res)


class TestPosts(DbTestCase, LoggedInUserCase):
    def setUp(self):
        self.w = TestApp(self.app)
        self.user = UserFactory(password="myprecious")
        self.user.save()

    def test_can_create(self):
        self._login(self.w, self.user)

        res = self.w.get(url_for("user.add_post"))

        form = res.forms["newPost"]

        form['title'] = "test post please ignore"
        form['subreddit'] = "reddit.com"
        form['body'] = "This is a test post."
        form['distinguish'] = False
        form['sticky'] = False
        form['scheduled_hour'] = 12
        form['scheduled_minute'] = 00

        res = form.submit().follow()
        assert_equal(res.status_code, 200)

    def test_can_submit_edit_form_without_changes(self):
        self._login(self.w, self.user)

        post = PostFactory()

        self.user.posts.append(post)
        self.user.save()

        res = self.w.get(url_for('user.edit_post', id=post.id))
        form = res.forms["newPost"]
        res = form.submit().follow()

    def test_can_edit(self):
        self._login(self.w, self.user)

        post = PostFactory()

        self.user.posts.append(post)
        self.user.save()

        res = self.w.get(url_for('user.edit_post', id=post.id))

        new_title = "this is a test title"

        form = res.forms["newPost"]

        previous_day_value = form['monday']

        form['title'] = new_title
        form['monday'] = not previous_day_value

        res = form.submit().follow()
        assert_equal(post.title, new_title)
        assert_equal(post.days.monday, not previous_day_value)
