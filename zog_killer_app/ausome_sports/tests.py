from django.contrib.auth.models import User 
from django.core import serializers
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import dateparse

from datetime import date, datetime
import json
from . import models, decorators, utils


# Create your tests here.
class LogInLogOutTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')

    def test_login_logout(self):
        response = self.client.get(reverse('user_profile')) 
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 401)

        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        response = self.client.get(reverse('user_profile')) 
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)

        self.client.get(reverse('logout'))
        
        response = self.client.get(reverse('user_profile')) 
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 401)

class UserProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')

    def test_user_profile(self):
        response = utils.verify_login_required(self, 'user_profile')
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)

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
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')
        cls.league = utils.create_ausome_league() 
    
    def test_leagues_by_sport_status_success(self):
        response = utils.verify_login_required(self, 'leagues_by_sport_status', args=['volleyball', 'open'])
        self.assertEqual(response['Content-Type'], 'application/json')

        data = serializers.serialize('json', [self.league])
        self.assertEqual(data, response.json())

    def test_leagues_by_sport_status_no_results(self):
        response = utils.verify_login_required(self, 'leagues_by_sport_status', args=['kickball', 'open'])
        self.assertEqual(response['Content-Type'], 'application/json')

        data = serializers.serialize('json', [])
        self.assertEqual(data, response.json())

class JoinTeamTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')
        
        cls.league = utils.create_ausome_league() 
        cls.closed_league = utils.create_ausome_league(status='closed') 
        cls.no_team_league = utils.create_ausome_league(team_max=0) 
        cls.team_random = utils.create_ausome_team(league=cls.no_team_league, creator=cls.ausome_user)

        cls.team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user)

        cls.user_team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user, team_type='U')
        cls.user_team.team_password = 'werock'
        cls.user_team.save()

        cls.open_team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user, team_type='U', payment_plan='team per person')
        cls.open_team.open_registration = True 
        cls.open_team.save()

        cls.no_player_team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user, team_type='U', player_max=0, payment_plan='team whole')
        cls.no_player_team.team_password = 'werock'
        
        cls.no_player_open_team = utils.create_ausome_team(league=cls.no_team_league, creator=cls.ausome_user, team_type='U', player_max=0, payment_plan='team per person')

    def test_verify_login_required(self):
        # verify that login is required
        response = self.client.post(reverse('create_team'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 401) 
    
    def test_join_random_team_success(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team': 'random',
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully joined!") 

        team_member = models.TeamMember.objects.get(team=self.team, user=self.ausome_user)

        self.assertTrue(team_member!= None)

    def test_join_specific_team_success(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team': str(self.user_team.pk),
                'team_password': 'werock',
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully joined!") 

        team_member = models.TeamMember.objects.get(team=self.user_team, user=self.ausome_user)

        self.assertTrue(team_member != None)

    def test_join_open_call_team_success(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team': str(self.open_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully joined!") 

        team_member = models.TeamMember.objects.get(team=self.open_team, user=self.ausome_user)

        self.assertTrue(team_member != None)

    def test_join_schema(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        # missing league parameter
        data = {
                'team': str(self.open_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "'league' is a required property") 

        # missing team parameter
        data = {'league': str(self.league.pk), 
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "'team' is a required property") 

    def test_join_no_league(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': "30", 
                'team': str(self.open_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "No league found with that id") 

    def test_join_league_closed(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.closed_league.pk), 
                'team': str(self.open_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, this league is not open for registration.") 

    def test_join_already_in_league(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team': str(self.open_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully joined!") 

        data = {'league': str(self.league.pk), 
                'team': str(self.open_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "You're already on a team in this league! Sorry, but you can only join one team per league.") 

    def test_join_no_team(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team': "30",
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "No team found in this league with that id") 

    def test_join_team_full(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team': str(self.no_player_team.pk),
                'team_password': 'werock',
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, but this team is full!") 

    def test_join_total_player_max(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.no_team_league.pk), 
                'team': str(self.no_player_open_team.pk),
                'team_password': 'werock',
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, but this league is full!") 

    def test_join_password(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        # missing password
        data = {'league': str(self.league.pk), 
                'team': str(self.user_team.pk),
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Please enter a password") 

        # bad password
        data = {'league': str(self.league.pk), 
                'team': str(self.user_team.pk),
                'team_password': 'thisiswrong',
                }

        response = self.client.post(reverse('join_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Whoops! Wrong password") 

class CreateTeamTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')
        cls.ausome_user_two = utils.create_ausome_user(username='testuser2', email='test2@test.com')
        cls.league = utils.create_ausome_league()
        cls.closed_league = utils.create_ausome_league(status='closed')
        cls.no_team_league = utils.create_ausome_league(team_max=0)
        cls.team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user)
        cls.no_player_league = utils.create_ausome_league(team_max=1)
        cls.no_player_team = utils.create_ausome_team(league=cls.no_player_league, creator=cls.ausome_user, player_max=0, team_type='U')
        cls.no_player_random_team = utils.create_ausome_team(league=cls.no_player_league, creator=cls.ausome_user, player_max=0, team_type='R')

    def test_verify_login_required(self):
        # verify that login is required
        response = self.client.post(reverse('create_team'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 401) 

    def test_create_team_whole_success(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully created a team!") 

        team = models.Team.objects.get(league=self.league, name=data['team_name'].lower())
        self.assertEqual(team.league.pk, int(data['league']))
        self.assertEqual(team.name, data['team_name'].lower())
        self.assertEqual(team.creator, self.ausome_user)
        self.assertEqual(team.team_password, data['team_password'])
        self.assertEqual(team.payment_plan, data['payment_plan'])

        team_member = team.teammember_set.filter()[0]
        self.assertEqual(team_member.user, self.ausome_user)

    def test_create_team_individual_success(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser2', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team_name': 'Mario Bros',
                'payment_plan': 'team per person',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully created a team!") 

        team = models.Team.objects.get(league=self.league, name=data['team_name'].lower())
        self.assertEqual(team.league.pk, int(data['league']))
        self.assertEqual(team.name, data['team_name'].lower())
        self.assertEqual(team.creator, self.ausome_user_two)
        self.assertEqual(team.payment_plan, data['payment_plan'])

        team_member = team.teammember_set.filter()[0]
        self.assertEqual(team_member.user, self.ausome_user_two)

    def test_create_team_missing_post_data(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser2', 'password': 'password99'}
            )

        # missing league
        data = {'team_name': 'Mario Bros',
                'payment_plan': 'team per person',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "'league' is a required property") 

        # missing team name
        data = {'league': str(self.league.pk), 
                'payment_plan': 'team per person',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "'team_name' is a required property") 

        # missing payment plan
        data = {'league': str(self.league.pk), 
                'team_name': 'Mario Bros',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "'payment_plan' is a required property") 

    def test_create_team_league_does_not_exits(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': '30', 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "No league found with that id") 

    def test_create_team_league_signup_closed(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.closed_league.pk), 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, this league is not open for registration.") 

    def test_create_team_user_already_in_a_team(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully created a team!") 

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "You're already on a team in this league! Sorry, but you can only join one team per league.") 

    def test_create_team_above_team_max(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.no_team_league.pk), 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, but this league is full") 

    def test_create_team_above_player_max(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.no_player_league.pk), 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team per person',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, but this league is at capacity") 

    def test_create_team_name_already_exists(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team_name': 'Mighty ducks',
                'team_password': 'password99',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['msg'], "You've successfully created a team!") 

        # log in with a different user
        self.client.post(reverse('post_login'), 
            {'username': 'testuser2', 'password': 'password99'}
            )

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Sorry, but this team name is taken") 

    def test_create_team_no_password(self):
        # log in
        self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

        data = {'league': str(self.league.pk), 
                'team_name': 'Mighty ducks',
                'payment_plan': 'team whole',
                }

        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], "Please enter a password") 

class UserTeamsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')
        cls.ausome_user_two = utils.create_ausome_user(username='testuser2', email='test2@test.com')
        cls.league = utils.create_ausome_league() 
        cls.team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user, team_type = 'U') 
        cls.team_member = models.TeamMember(team=cls.team, user=cls.ausome_user)
        cls.team_member.save()

    def test_verify_login_required(self):
        # verify that login is required
        response = self.client.post(reverse('user_teams'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 401) 
    
    def test_get_teams_success(self):
        # log in
        self.client.post(reverse('post_login'), 
                {'username': 'testuser', 'password': 'password99'}
                )

        user_team_members = self.ausome_user.teammember_set.all()
        user_teams = [tm.team for tm in user_team_members] 
        user_leagues = [t.league for t in user_teams]

        user_teams = serializers.serialize('json', user_teams) 
        user_leagues = serializers.serialize('json', user_leagues) 
        data = {'leagues': user_leagues,
                'teams': user_teams,
                }

        response = self.client.get(reverse('user_teams'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data) 

    def test_get_teams_empty(self):
        # log in
        self.client.post(reverse('post_login'), 
                {'username': 'testuser2', 'password': 'password99'}
                )

        user_team_members = self.ausome_user_two.teammember_set.all()
        user_teams = [tm.team for tm in user_team_members] 
        user_leagues = [t.league for t in user_teams]

        user_teams = serializers.serialize('json', user_teams) 
        user_leagues = serializers.serialize('json', user_leagues) 
        data = {'leagues': user_leagues,
                'teams': user_teams,
                }
        
        response = self.client.get(reverse('user_teams'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data) 

class UserTeamGamesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ausome_user = utils.create_ausome_user(username='testuser', email='test@test.com')
        cls.ausome_user_two = utils.create_ausome_user(username='testuser2', email='test2@test.com')
        cls.league = utils.create_ausome_league() 
        cls.team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user, team_type = 'U') 
        cls.team_member = models.TeamMember(team=cls.team, user=cls.ausome_user)
        cls.team_member.save()
        cls.game = utils.create_ausome_game(league=cls.league) 
        cls.game.teams.add(cls.team)

        cls.empty_team = utils.create_ausome_team(league=cls.league, creator=cls.ausome_user, team_type = 'U') 

    def test_verify_login_required(self):
        # verify that login is required
        response = self.client.post(reverse('user_teams'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 401) 
    
    def test_get_team_games(self):
        # log in
        self.client.post(reverse('post_login'), 
                {'username': 'testuser', 'password': 'password99'}
                )

        data = self.team.game_set.all() 
        data = serializers.serialize('json', data)

        response = self.client.get(reverse('team_games', args=[str(self.league.pk), str(self.team.pk)]))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)

    def test_no_league(self):
        # log in
        self.client.post(reverse('post_login'), 
                {'username': 'testuser', 'password': 'password99'}
                )

        response = self.client.get(reverse('team_games', args=["55", str(self.team.pk)]))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'No league found with that id')

    def test_no_team(self):
        # log in
        self.client.post(reverse('post_login'), 
                {'username': 'testuser', 'password': 'password99'}
                )

        response = self.client.get(reverse('team_games', args=[str(self.league.pk), "55"]))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'No team found with that id')

    def test_user_not_on_team(self):
        # log in
        self.client.post(reverse('post_login'), 
                {'username': 'testuser', 'password': 'password99'}
                )

        response = self.client.get(reverse('team_games', args=[str(self.league.pk), str(self.empty_team.pk)]))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['msg'], "You're not allowed to access this team's games")
