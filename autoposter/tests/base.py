# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase
from autoposter.settings import TestConfig
from autoposter.app import create_app
from autoposter.database import db


class DbTestCase(TestCase):
    """Base TestCase for tests that require a database."""

    def create_app(self):
        app = create_app(TestConfig)
        with app.app_context():
            db.create_all()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class LoggedInUserCase(TestCase):
    """Provides a login method to easily authorize session"""

    def _login(self, app, user):
        with app.session_transaction() as session:
            session['user_id'] = user.id
