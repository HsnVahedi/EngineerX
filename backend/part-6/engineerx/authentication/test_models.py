from faker import Faker

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError

from modules import fakedata

User = get_user_model()
fake = Faker()


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        fakedata.create_users(5)

    def test_creating_user_with_existing_email_raises_error(self):
        new_user = fakedata.FakeUser(fake.profile(), fake.password())
        existing_user = User.objects.first()
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=existing_user.email,
                username=new_user.username, password=new_user.password,
                first_name=new_user.first_name, last_name=new_user.last_name,
            )
