from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse
from django.utils import dateparse

from datetime import date, datetime
from . import models

def verify_login_required(self, view_name, args=None):
    response = self.client.get(reverse(view_name, args=args))
    self.assertEqual(response.status_code, 403)

    self.client.post(reverse('post_login'), 
            {'username': 'testuser', 'password': 'password99'}
            )

    response = self.client.get(reverse(view_name, args=args))
    self.assertEqual(response.status_code, 200)
    return response


def create_ausome_user(username, email):
    auth_user = User.objects.create_user(username=username,
            email=email,
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

def create_ausome_league(status='open', team_max=10):
    league = models.League() 
    league.name = 'Beach Volleyball'
    league.sport = 'volleyball'
    league.city = 'Austin'
    league.state = 'TX'
    league.country = 'US'
    league.start_date = dateparse.parse_date('2016-06-15') 
    league.end_date = dateparse.parse_date('2016-08-15') 
    league.description = 'Advanced beach volleyball played Wednesday nights at Zilker park'
    league.difficulty = 'advanced'
    league.status = status 
    league.team_max = team_max 
    league.save()

    return league
    
def create_ausome_team(league=None, creator=None, player_max=10, team_type='R', payment_plan='individual'):
    team = models.Team()
    team.name = 'Awaiting assignment'
    team.league = league
    team.creator = creator
    team.team_type = team_type 
    team.player_max = player_max 
    team.payment_plan = payment_plan 
    team.open_registration = False
    team.save()

    return team
    
