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
        u = User(username='testuser2', email='test.user@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/a775546e5a4e4ac660cd78a61cd90bb3?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')
        self.assertEqual(u2.followed.count(), 0)

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='1', email='1@one.com')
        u2 = User(username='2', email='2@one.com')
        u3 = User(username='3', email='3@one.com')
        u4 = User(username='4', email='4@one.com')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(body='Post of 1', author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body='Post of 2', author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body='Post of 3', author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body='Post of 4', author=u4, timestamp=now + timedelta(seconds=2))

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)
