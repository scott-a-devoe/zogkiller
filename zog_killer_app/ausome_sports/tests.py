from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse
from django.test import TestCase
from datetime import date, datetime
from . import models, decorators

def create_ausome_user():
    auth_user = User.objects.create_user(username='testuser',
            email='test@test.com',
            password='password',
            )
    ausome_user = models.AusomeUser()
    ausome_user.user = auth_user
    ausome_user.email = auth_user.email
    ausome_user.first_name = 'First'
    ausome_user.last_name = 'Last'
    ausome_user.dob = date.today() 
    ausome_user.sex = 'male'
    ausome_user.picture = 'example.jpg'
    ausome_user.bio = 'Spike it real good!'
    ausome_user.visible_in_directory = True
    ausome_user.save()

    return ausome_user


# Create your tests here.
class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = create_ausome_user()

    def verify_login_required(self, view_name):
        response = self.client.get(reverse(view_name))
        self.assertEqual(response.status_code, 403)

        self.client.post(reverse('post_login'), 
                {'username': 'testuser', 'password': 'password'}
                )

        response = self.client.get(reverse(view_name))
        self.assertEqual(response.status_code, 200)
        return response
    
    def test_user_profile(self):
        response = self.verify_login_required('user_profile')
