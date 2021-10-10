"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql+psycopg2://postgres:qwerty@localhost:5432/warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_create_user(self):
        """Does User.create successfully create a new user given valid credentials?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(User.query.all()), 1)
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_in_user_model(self):
        """Does the repr method return the expected formatted string"""

        u = User(email="test@test.com",
                 username="testuser",
                 password="Hashed_pass")

        self.assertEqual(repr(u), "<User #None: testuser, test@test.com>")

    def test_user1_is_following_user2(self):
        """Does is_following successfully detect when user1 is following user2?"""

        user1 = User(email="user1@test.com",
                     username="user1",
                     password="password")

        user2 = User(email="user2@test.com",
                     username="user2",
                     password="password")

        db.session.add(user1, user2)
        db.session.commit()

        user1.following.append(user2)
        self.assertTrue(user1.is_following(user2))

    def test_user1_is_not_following_user2(self):
        """Does is_following successfully detect when user1 is not following user2?"""

        user1 = User(email="user1@test.com",
                     username="user1",
                     password="password")

        user2 = User(email="user2@test.com",
                     username="user2",
                     password="password")

        db.session.add(user1, user2)
        db.session.commit()

        self.assertFalse(user1.is_following(user2))

    def test_user2_is_followed_by_user1(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        user1 = User(email="user1@test.com",
                     username="user1",
                     password="password")

        user2 = User(email="user2@test.com",
                     username="user2",
                     password="password")

        db.session.add(user1, user2)
        db.session.commit()
        user1.following.append(user2)

        self.assertFalse(user2.is_followed_by(user1))

    def test_user2_is_not_followed_by_user1(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""

        user1 = User(email="user1@test.com",
                     username="user1",
                     password="password")

        user2 = User(email="user2@test.com",
                     username="user2",
                     password="password")

        db.session.add(user1, user2)
        db.session.commit()

        self.assertFalse(user2.is_followed_by(user1))
