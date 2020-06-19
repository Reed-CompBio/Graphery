from django.db import IntegrityError
from django.test import TestCase
from backend.models import User, ROLES


class UserTest(TestCase):
    def test_set_up_normal_user(self):
        User.objects.create_user('test@reed.edu', 'test_acc', 'password', role=ROLES.VISITOR)
        self.assertEqual(User.objects.get(email='test@reed.edu'), User.objects.get(username='test_acc'))

    def test_same_username(self):
        User.objects.create_user('test@reed.edu', 'test_acc', 'password', role=ROLES.VISITOR)
        with self.assertRaises(IntegrityError):
            User.objects.create_user('test1@reed.edu', 'test_acc', 'password')

    def test_same_email(self):
        User.objects.create_user('test@reed.edu', 'test_acc', 'password', role=ROLES.VISITOR)
        with self.assertRaises(IntegrityError):
            User.objects.create_user('test@reed.edu', 'test_acc1', 'password')
