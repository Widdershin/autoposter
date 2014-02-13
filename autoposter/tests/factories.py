# -*- coding: utf-8 -*-
from factory import (Sequence, PostGenerationMethodCall,
                     LazyAttribute, lazy_attribute)
from factory.alchemy import SQLAlchemyModelFactory
import random

from autoposter.user.models import User, Post, DaysOfWeek
from autoposter.database import db


@lazy_attribute
def random_days(self):
    return [random.choice([True, False]) for _ in range(7)]


class UserFactory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session
    FACTORY_FOR = User

    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall("set_password", 'example')
    active = True


class DaysOfWeekFactory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session
    FACTORY_FOR = DaysOfWeek

    days = random_days


class PostFactory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session
    FACTORY_FOR = Post

    title = "test post please ignore"
    subreddit = "widdershiny"
    body = "This is a test post..."
    days = [True] * 7
    distinguish = random.choice([True, False])
    sticky = random.choice([True, False])
