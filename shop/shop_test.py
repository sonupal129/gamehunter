from django.urls import resolve, reverse
from django.test import TestCase

class SignUpViewTest(TestCase):
    def test_signup_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)