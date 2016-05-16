from django.contrib.auth.models import User 
from django.core import serializers
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import dateparse

from datetime import date, datetime
import json
from . import models, decorators

def create_ausome_user():
    auth_user = User.objects.create_user(username='testuser',
            email='test@test.com',
            password='password99',
            )
    ausome_user = models.AusomeUser()
    ausome_user.user = auth_user
    ausome_user.email = auth_user.email
    ausome_user.first_name = 'First'
    ausome_user.last_name = 'Last'
    ausome_user.dob = dateparse.parse_date('1990-01-02')
    ausome_user.sex = 'male'
    ausome_user.picture = 'example.jpg'
    ausome_user.phone = '12334556788'
    ausome_user.bio = 'Spike it real good!'
    ausome_user.visible_in_directory = True
    ausome_user.save()

    return ausome_user

def verify_login_required(self, view_name, args=None):
    response = self.client.get(reverse(view_name, args=args))
    self.assertEqual(response.status_code, 403)

    self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

    response = self.client.get(reverse(view_name, args=args))
    self.assertEqual(response.status_code, 200)
    return response


# Create your tests here.
class UserProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = create_ausome_user()

    def test_user_profile(self):
        response = verify_login_required(self, 'user_profile')
        self.assertEqual(response['Content-Type'], 'application/json')

class AccountCreationTest(TestCase):

    def test_create_account_success(self):
        # Only includes info needed for account creation, not all possible info
        data = {'username': 'testuser',
                'email': 'test@test.com',
                'password': 'password99',
                'first_name': 'First',
                'last_name': 'Last',
                'dob': '1990-01-02',
                'sex': 'male',
                'phone': '12334556788',
                'visible_in_directory': 'y',
                }
        response = self.client.post(reverse('create_user'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['msg'], 'Account created!')

        auth_user = User.objects.all()[0]
        ausome_user = models.AusomeUser.objects.get(user=auth_user) 
        self.assertEqual(auth_user, ausome_user.user) 
        self.assertEqual(ausome_user.user.username, 'testuser')
        self.assertEqual(ausome_user.email, 'test@test.com')
        self.assertEqual(ausome_user.first_name, 'First')
        self.assertEqual(ausome_user.last_name, 'Last')
        self.assertEqual(ausome_user.dob, dateparse.parse_date('1990-01-02'))
        self.assertEqual(ausome_user.sex, 'male')
        self.assertEqual(ausome_user.phone, '12334556788')
        self.assertEqual(ausome_user.visible_in_directory, True)

class ProfileUpdateTest(TestCase):

    def test_update_profile_success(self):
        data = {'username': 'testuser',
                'email': 'test@test.com',
                'password': 'password99',
                'first_name': 'First',
                'last_name': 'Last',
                'dob': '1990-01-02',
                'sex': 'male',
                'phone': '12334556788',
                'visible_in_directory': 'y',
                }
        response = self.client.post(reverse('create_user'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['msg'], 'Account created!')
        
        response = self.client.post(reverse('post_login'), {'username': 'testuser', 'password': 'password99'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['msg'], 'Success!')

        data = {'username': 'updatedtestuser',
                'email': 'updatedtest@test.com',
                'first_name': 'Updatedfirst',
                'last_name': 'UpdatedLast',
                'dob': '1991-02-03',
                'sex': 'female',
                'bio': 'Spike it real good!',
                'picture': 'example.jpg',
                'phone': '12334556789',
                'visible_in_directory': 'n',
                }
        response = self.client.post(reverse('update_profile'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['msg'], 'Profile updated!')

        auth_user = User.objects.all()[0]
        ausome_user = models.AusomeUser.objects.get(user=auth_user) 
        self.assertEqual(auth_user, ausome_user.user) 
        self.assertEqual(ausome_user.user.username, 'updatedtestuser')
        self.assertEqual(ausome_user.email, 'updatedtest@test.com')
        self.assertEqual(ausome_user.first_name, 'Updatedfirst')
        self.assertEqual(ausome_user.last_name, 'UpdatedLast')
        self.assertEqual(ausome_user.dob, dateparse.parse_date('1991-02-03'))
        self.assertEqual(ausome_user.sex, 'female')
        self.assertEqual(ausome_user.bio, 'Spike it real good!')
        self.assertEqual(ausome_user.picture, 'example.jpg')
        self.assertEqual(ausome_user.phone, '12334556789')
        self.assertEqual(ausome_user.visible_in_directory, False)

class LeaguesBySportStatusTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = create_ausome_user()

        cls.league = models.League() 
        cls.league.name = 'Beach Volleyball'
        cls.league.sport = 'volleyball'
        cls.league.city = 'Austin'
        cls.league.state = 'TX'
        cls.league.country = 'US'
        cls.league.start_date = dateparse.parse_date('2016-06-15') 
        cls.league.end_date = dateparse.parse_date('2016-08-15') 
        cls.league.description = 'Advanced beach volleyball played Wednesday nights at Zilker park'
        cls.league.difficulty = 'advanced'
        cls.league.status = 'open'
        cls.league.team_max = 10
        cls.league.date_added = dateparse.parse_datetime('2000-08-02 14:00:00') 
        cls.league.save()
    
    def test_leagues_by_sport_status_success(self):
        response = verify_login_required(self, 'leagues_by_sport_status', args=['volleyball', 'open'])
        self.assertEqual(response['Content-Type'], 'application/json')

        data = serializers.serialize('json', [self.league])
        self.assertEqual(data, response.json())

    def test_leagues_by_sport_status_no_results(self):
        response = verify_login_required(self, 'leagues_by_sport_status', args=['kickball', 'open'])
        self.assertEqual(response['Content-Type'], 'application/json')

        data = serializers.serialize('json', [])
        self.assertEqual(data, response.json())

class JoinRandomTeamTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = create_ausome_user()

        cls.league = models.League() 
        cls.league.name = 'Beach Volleyball'
        cls.league.sport = 'volleyball'
        cls.league.city = 'Austin'
        cls.league.state = 'TX'
        cls.league.country = 'US'
        cls.league.start_date = dateparse.parse_date('2016-06-15') 
        cls.league.end_date = dateparse.parse_date('2016-08-15') 
        cls.league.description = 'Advanced beach volleyball played Wednesday nights at Zilker park'
        cls.league.difficulty = 'advanced'
        cls.league.status = 'open'
        cls.league.team_max = 10
        cls.league.save()

        cls.team = models.Team()
        cls.team.name = 'Awaiting assignment'
        cls.team.league = cls.league
        cls.team.creator = cls.ausome_user
        cls.team.team_type = 'R'
        cls.team.player_max = 10 
        cls.team.open_registration = False
        cls.team.save()
    
    def test_join_random_team_success(self):
        # verify that login is required
        data = {'league': str(self.league.pk), 'team': str(self.team.pk),}
        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')

        self.assertEqual(response.status_code, 403) 

        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully joined!") 

        team_member = models.TeamMember.objects.get(user=self.ausome_user)

        self.assertTrue(team_member!= None)
        self.assertTrue(team_member.team == self.team)

    def test_join_specific_team_success(self):
        pass

    def test_join_open_call_team_success(self):
        pass

    def test_already_joined_team(self):
        pass
