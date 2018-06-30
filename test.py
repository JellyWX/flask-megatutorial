from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='testuser1')
        u.set_password('DogCatCatDog')
        self.assertFalse(u.check_password('CatDogDogCat'))
        self.assertTrue(u.check_password('DogCatCatDog'))

    def test_avatar(self):
        u = User(username='testuser2', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/a775546e5a4e4ac660cd78a61cd90bb3?d=identicon&s=128'))

    def test_follow(self):
        pass

    def test_follow_posts(self):
        pass
