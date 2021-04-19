from django.test import TestCase

from myproject.accounts.models import User
from myproject.crm.models import Phone


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@email.com',
            password='demodemo',
            first_name='Admin',
            last_name='Admin',
        )
        self.phone = Phone.objects.create(
            phone='9876-54321',
            user=self.user
        )

    def test_phone_exists(self):
        self.assertTrue(self.phone)

    def test_str(self):
        self.assertEqual(self.user.email, 'admin@email.com')
