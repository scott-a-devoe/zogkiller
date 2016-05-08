from django.conf import settings
from django.db import models

# Create your models here.

class AusomeUser(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100) 
    dob = models.DateField() 
    sex = models.CharField(max_length=6, choices=[('M', 'Male'), ('W', 'Female'),]) 
    email = models.CharField(max_length=100) 
    active = models.BooleanField() 
    picture = models.CharField(max_length=100)  
    bio = models.CharField(max_length=500)  
    visible_in_directory = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass

class League(models.Model):

    name = models.TextField()
    sport = models.CharField(max_length=20, choices=[('volleyball', 'Volleyball'),])
    city = models.CharField(max_length=100) 
    state = models.CharField(max_length=100) 
    country = models.CharField(max_length=2) 
    start_date = models.DateField() 
    end_date = models.DateField() 
    description = models.TextField() 
    difficulty = models.CharField(max_length=20) 
    status = models.CharField(max_length=20) 
    date_added = models.DateTimeField(auto_now_add=True) 
    
    def natural_key(self):
        pass

    def __repr__(self):
        pass


class Team(models.Model):

    name = models.CharField(max_length=50) 
    league = models.ForeignKey(League, on_delete=models.CASCADE) 
    creator = models.ManyToManyField(AusomeUser, null=True, blank=True) 
    team_type = models.CharField(max_length=15, choices=[('R', 'Random'), ('U', 'User Generated'),]) 
    open_registration = models.BooleanField(default=False) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass

class TeamMember(models.Model):

    user = models.ForeignKey(AusomeUser, on_delete=models.CASCADE) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE) 
    is_captain = models.BooleanField(default=False) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass

class PendingTeamMember(models.Model):

    user = models.ForeignKey(AusomeUser, on_delete=models.CASCADE) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass

class Game(models.Model):

    league = models.ForeignKey(League, on_delete=models.CASCADE) 
    teams = models.ManyToManyField(Team, null=True, blank=True) 
    date = models.DateTimeField() 
    location = models.TextField() 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass

class Win(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True) 
    game = models.ForeignKey(Game, on_delete=models.CASCADE) 
    score = models.CharField(max_length=50, null=True, blank=True) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass

class Loss(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True) 
    game = models.ForeignKey(Game, on_delete=models.CASCADE) 
    score = models.CharField(max_length=50, null=True, blank=True) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __repr__(self):
        pass
