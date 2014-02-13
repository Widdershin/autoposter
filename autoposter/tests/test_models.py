# -*- coding: utf-8 -*-
import unittest
from nose.tools import *  # PEP8 asserts

from autoposter.database import db
from autoposter.user.models import User, Post
from .base import DbTestCase
from .factories import UserFactory, DaysOfWeekFactory, PostFactory


class TestUser(DbTestCase):

    def test_factory(self):
        user = UserFactory(password="myprecious")
        assert_true(user.username)
        assert_true(user.email)
        assert_true(user.created_at)
        assert_false(user.is_admin)
        assert_true(user.active)
        assert_true(user.check_password("myprecious"))

    def test_check_password(self):
        user = User.create(username="foo", email="foo@bar.com",
                           password="foobarbaz123")
        assert_true(user.check_password('foobarbaz123'))
        assert_false(user.check_password("barfoobaz"))

    def test_full_name(self):
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert_equal(user.full_name, "Foo Bar")


class TestDaysOfWeek(DbTestCase):

    def test_factory(self):
        days = DaysOfWeekFactory()
        assert_in(days.wednesday, [True, False])

    def test_iter(self):
        days = DaysOfWeekFactory()

        for day in days:
            assert_in(day, [True, False])

    def test_specific_day(self):
        day_list = [True] + [False] * 6

        days = DaysOfWeekFactory(days=day_list)

        assert_true(days.monday)
        assert_false(days.friday)


class TestPost(DbTestCase):

    def test_factory(self):
        post = PostFactory()

        assert_true(post.title)
        assert_true(post.body)
        assert_true(post.subreddit)

    def test_days(self):
        post = PostFactory(days=[True] + [False] * 6)

        assert_true(post.days.monday)
        assert_false(post.days.sunday)


if __name__ == '__main__':
    unittest.main()
