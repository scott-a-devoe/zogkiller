import bleach
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonValidationError
from . import models, decorators, schema

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password
from django.core import serializers
from django.core.exceptions import ValidationError as DjangoValidationError 
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import dateparse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie 

@ensure_csrf_cookie
def index(request):
    return render(request, 'ausome_sports/index.html')

@decorators.login_required
def get_user_profile(request):
    profile_set = models.AusomeUser.objects.filter(user=request.user)
    data = serializers.serialize('json', profile_set)

    return HttpResponse(data, content_type='application/json')

@require_POST
def post_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            data = {'msg': 'Success!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'msg': 'Account disabled'}
            denied = HttpResponse(json.dumps(data), content_type='application/json')
            denied.status_code = 401
            return denied 
    else:
        data = {'msg': 'Username and/or password incorrect'}
        denied = HttpResponse(json.dumps(data), content_type='application/json')
        denied.status_code = 401
        return denied 

@require_POST
def post_create_user(request):

    # Validate POST contents
    try:
        validate(request.POST, schema.new_account)
    except JsonValidationError as error:
        error_msg = error.schema.get('error_msg')
        data = {'msg': error_msg if error_msg != None else error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    username = bleach.clean(request.POST.get('username'))
    email = bleach.clean(request.POST.get('email'))

    # check for existing username or email address
    if User.objects.filter(username=username).exists():
        data = {'msg': 'Username already exists'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 
    elif User.objects.filter(email=email).exists():
        data = {'msg': 'An account already exists with that e-mail address'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    
    password = request.POST.get('password')
    # validate password
    try:
        validate_password(password)
    except DjangoValidationError as error:
        data = {'msg': error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # create auth user
    user = User.objects.create_user(username,
            email,
            password,
            )
    ausome_user = models.AusomeUser(user=user, email=user.email)
    ausome_user.first_name = bleach.clean(request.POST.get('first_name'))
    ausome_user.last_name = bleach.clean(request.POST.get('last_name'))

    # attempt to parse date string
    try:
        ausome_user.dob = dateparse.parse_date(request.POST.get('dob'))
    except ValueError as error:
        data = {'msg': error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    ausome_user.sex = bleach.clean(request.POST.get('sex')).lower()
    ausome_user.phone = bleach.clean(request.POST.get('phone'))
    ausome_user.visible_in_directory = True if request.POST.get('visible_in_directory').lower() == 'y' else False 

    # attempt to save to database
    try:
        ausome_user.save()
    except:
        data = {'msg': 'Account creation failed!'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    data = {'msg': 'Account created!'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@require_POST
@decorators.login_required
def post_update_profile(request):
    # Does not update password

    # Validate POST contents
    try:
        validate(request.POST, schema.update_account)
    except JsonValidationError as error:
        error_msg = error.schema.get('error_msg')
        data = {'msg': error_msg if error_msg != None else error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    profile_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'dob': request.POST.get('dob'),
            'sex': request.POST.get('sex'),
            'bio': request.POST.get('bio'),
            'picture': request.POST.get('picture'),
            'phone': request.POST.get('phone'),
            'visible_in_directory': request.POST.get('visible_in_directory'),
        }

    if profile_data['username'] != None:
        profile_data['username'] = bleach.clean(profile_data['username'])
        # check for existing username
        if User.objects.filter(username=profile_data['username']).exists():
            data = {'msg': 'Username already exists'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 
    elif profile_data['email'] != None:
        # check for existing email address
        profile_data['email'] = bleach.clean(profile_data['email'])
        if User.objects.filter(email=profile_data['email']).exists():
            data = {'msg': 'An account already exists with that e-mail address'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 
    elif profile_data['dob'] != None:
        # attempt to parse date string
        try:
            profile_data['dob'] = dateparse.parse_date(profile_data['dob'])
        except ValueError as error:
            data = {'msg': error.message}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 

    ausome_user = models.AusomeUser.objects.get(user=request.user)

    for key in profile_data.keys():
        if key == 'username' and profile_data[key] != None:
            ausome_user.user.username = profile_data[key] 
        if key == 'email' and profile_data[key] != None:
            ausome_user.user.email = profile_data[key] 
            ausome_user.email = profile_data[key] 
        elif key == 'first_name' and profile_data[key] != None:
            ausome_user.first_name = bleach.clean(profile_data[key])
        elif key == 'last_name' and profile_data[key] != None:
            ausome_user.last_name = bleach.clean(profile_data[key])
        elif key == 'dob' and profile_data[key] != None:
            ausome_user.dob = profile_data[key]
        elif key == 'sex' and profile_data[key] != None:
            ausome_user.sex = bleach.clean(profile_data[key])
        elif key == 'bio' and profile_data[key] != None:
            ausome_user.bio = bleach.clean(profile_data[key])
        elif key == 'picture' and profile_data[key] != None:
            ausome_user.picture = bleach.clean(profile_data[key])
        elif key == 'phone' and profile_data[key] != None:
            ausome_user.phone = bleach.clean(profile_data[key])
        elif key == 'visible_in_directory' and profile_data[key] != None:
            ausome_user.visible_in_directory = True if profile_data[key].lower() == 'y' else False

    # attempt to save to database
    try:
        ausome_user.user.save()
        ausome_user.save()
    except:
        data = {'msg': 'Profile update failed!'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    data = {'msg': 'Profile updated!'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@decorators.login_required
def get_leagues_by_sport_status(request, sport, status):
    league_set = models.League.objects.filter(sport=sport, status=status)
    data = serializers.serialize('json', league_set)
    
    return HttpResponse(json.dumps(data), content_type='application/json')

@require_POST
@decorators.login_required
def post_join_team(request):
    # validate schema contains league # and team id (digits or the word random) and optionally team password  
    try: 
        validate(request.POST, schema.join_team)
    except JsonValidationError as error:
        error_msg = error.schema.get('error_msg')
        data = {'msg': error_msg if error_msg != None else error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # check if league exists 
    league_id = int(request.POST['league'])
    try:
        league = models.League.objects.get(pk=league_id)
    except models.League.DoesNotExist:
        data = {'msg': 'No league found with that id'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # check if league registration still open 
    if league.status != 'open':
        data = {'msg': 'Sorry, this league is not open for registration.'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # check if user is already a member of a team in this league
    ausome_user = models.AusomeUser.objects.get(user=request.user)
    all_team_members = models.TeamMember.objects.filter(user=ausome_user)
    teams = [member.team for member in all_team_members]
    league_ids = [t.league.pk for t in teams]
    if league_id in league_ids: 
        data = {'msg': "You're already on a team in this league! Sorry, but you can only join one team per league."}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # check if team exists in league and team not full if not random or open call then sign up 
    if request.POST['team'] != 'random':
        team_id = int(request.POST['team'])
        try:
            team = models.Team.objects.get(league=league, pk=team_id)
        except models.Team.DoesNotExist:
            data = {'msg': 'No team found in this league with that id'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 

        # check if team is full only for teams who paid in full. Team per person doesn't get this. 
        if team.payment_plan == 'team whole':
            team_member_count = models.TeamMember.objects.filter(team=team).count()
            if team_member_count >= team.player_max:
                data = {'msg': 'Sorry, but this team is full!'}
                invalid = HttpResponse(json.dumps(data), content_type='application/json')
                invalid.status_code = 400
                return invalid 
    else:
        # get random team object
        try:
            team = models.Team.objects.get(league=league,team_type='R')
        except models.Team.DoesNotExist:
            data = {'msg': 'No team found in this league with that id'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 

    # if random user or paying team per person check that current teams plus random signup is less than limit
    if team.team_type == 'R' or team.payment_plan == 'team per person': 
        max_players = team.player_max * league.team_max 
        paid_team_slots = models.Team.objects.filter(team_type='U', payment_plan='team whole').count() * team.player_max
        random_team = team if team.team_type == 'R' else models.Team.objects.filter(league=league, team_type='R')[0]
        random_players = models.TeamMember.objects.filter(team=random_team).count() 
        other_team_slots = 0
        other_teams = models.Team.objects.filter(league=league, team_type='U', payment_plan='team per person')
        for ot in other_teams:
            other_team_slots = other_team_slots + ot.teammember_set.count()
        total_players = paid_team_slots + other_team_slots + random_players
        if total_players >= max_players:
            data = {'msg': 'Sorry, but this league is full!'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 

    # add user to random team or open_call team
    if team.team_type == 'R' or team.payment_plan == "team per person":
        new_team_member = models.TeamMember(user=ausome_user, team=team)
    else:
        # add user to password protected team
        password = request.POST.get('team_password') 
        if team.team_password == 'NULL':
            data = {'msg': "That's odd. There's no password set."}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 
        elif password == None:
            data = {'msg': 'Please enter a password'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 
        elif password != team.team_password:
            data = {'msg': 'Whoops! Wrong password'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 

        new_team_member = models.TeamMember(user=ausome_user, team=team)

    try:
        new_team_member.save()
    except:
        data = {'msg': 'Unable to join team'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    data = {'msg': "You've successfully joined!"}
    return HttpResponse(json.dumps(data), content_type='application/json')

@require_POST
@decorators.login_required
def post_create_team(request):
    # validate schema contains league # and team id (digits or the word random) and optionally team password  
    try: 
        validate(request.POST, schema.create_team)
    except JsonValidationError as error:
        error_msg = error.schema.get('error_msg')
        data = {'msg': error_msg if error_msg != None else error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # check if league exists 
    league_id = int(request.POST['league'])
    try:
        league = models.League.objects.get(pk=league_id)
    except models.League.DoesNotExist:
        data = {'msg': 'No league found with that id'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # check if league registration still open 
    if league.status != 'open':
        data = {'msg': 'Sorry, this league is not open for registration.'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # ensure user not already on a team in this league
    ausome_user = models.AusomeUser.objects.get(user=request.user)
    all_team_members = models.TeamMember.objects.filter(user=ausome_user)
    teams = [member.team for member in all_team_members]
    league_ids = [t.league.pk for t in teams]
    if league_id in league_ids: 
        data = {'msg': "You're already on a team in this league! Sorry, but you can only join one team per league."}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # ensure below team max for league if paying for whole team
    current_team_count = models.Team.objects.filter(league=league, payment_plan='team whole').count()
    if current_team_count >= league.team_max:
        data = {'msg': "Sorry, but this league is full"}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # ensure below player max for league if creating team but paying by individual 
    random_team = models.Team.objects.filter(league=league, team_type='R')[0]
    if request.POST['payment_plan'] == 'team per person': 
        random_team = models.Team.objects.filter(league=league, team_type='R')[0]
        player_max = random_team.player_max
        max_players = player_max * league.team_max 
        paid_team_slots = models.Team.objects.filter(team_type='U', payment_plan='team whole').count() * player_max
        random_players = random_team.teammember_set.count() 
        other_team_slots = 0
        other_teams = models.Team.objects.filter(league=league, team_type='U', payment_plan='team per person')
        for ot in other_teams:
            other_team_slots = other_team_slots + ot.teammember_set.count()
        total_players = paid_team_slots + other_team_slots + random_players
        if total_players >= max_players:
            data = {'msg': 'Sorry, but this league is at capacity'}
            invalid = HttpResponse(json.dumps(data), content_type='application/json')
            invalid.status_code = 400
            return invalid 

    # ensure unique team name
    team_name = request.POST['team_name'].lower()
    if models.Team.objects.filter(name=team_name).exists():
        data = {'msg': 'Sorry, but this team name is taken'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # ensure password if team paying in full
    password = request.POST.get('team_password') 
    if password == None and request.POST['payment_plan'] == 'team whole':
        data = {'msg': 'Please enter a password'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    # create team and add user to team
    new_team = models.Team()
    new_team.name = team_name
    new_team.league = league
    new_team.creator = ausome_user
    # creates mad coupling
    new_team.player_max = random_team.player_max
    new_team.team_type = 'U'
    new_team.payment_plan = request.POST['payment_plan'] 
    if request.POST['payment_plan'] == 'team whole':
        new_team.team_password = password
    if request.POST['payment_plan'] == 'team per person':
        new_team.open_registration = True

    try:
        new_team.save()
    except:
        data = {'msg': 'Unable to create team'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    new_team_member = models.TeamMember()
    new_team_member.user = ausome_user
    new_team_member.team = new_team
    new_team_member.is_captain = True 

    try:
        new_team_member.save()
    except:
        data = {'msg': 'Team created, but unable to add you to it'}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    data = {'msg': "You've successfully created a team!"}
    return HttpResponse(json.dumps(data), content_type='application/json')
