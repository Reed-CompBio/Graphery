from django.test import TestCase
from backend.models import User, ROLES


class UserTest(TestCase):
    def test_set_up_normal_user(self):
        User.objects.create_user('test@reed.edu', 'test_acc', 'password', role=ROLES.VISITOR)
