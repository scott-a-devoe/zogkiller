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
    picture = models.CharField(max_length=100, null=True, blank=True)  
    phone = models.CharField(max_length=100)  
    bio = models.CharField(max_length=500, null=True, blank=True)  
    visible_in_directory = models.BooleanField(default=True)

    def natural_key(self):
        pass

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class League(models.Model):

    name = models.TextField()
    sport = models.CharField(max_length=20, choices=[('volleyball', 'Volleyball'),])
    city = models.CharField(max_length=100) 
    state = models.CharField(max_length=100) 
    country = models.CharField(max_length=2) 
    start_date = models.DateField() 
    end_date = models.DateField() 
    reg_date = models.DateField()
    day_of_week = models.CharField(max_length=100)
    indoor_outdoor = models.CharField(max_length=20)
    description = models.TextField() 
    location = models.TextField() 
    difficulty = models.CharField(max_length=20) 
    status = models.CharField(max_length=20) 
    team_max = models.IntegerField() 
    team_price = models.CharField(max_length=10)
    individual_price = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True) 
    
    def natural_key(self):
        pass

    def __str__(self):
        return self.name

class Team(models.Model):

    name = models.CharField(max_length=50) 
    league = models.ForeignKey(League, on_delete=models.CASCADE) 
    creator = models.ForeignKey(AusomeUser) 
    team_type = models.CharField(max_length=15, choices=[('R', 'Random'), 
        ('U', 'User generated'),
        ]) 
    open_registration = models.BooleanField(default=False) 
    team_password = models.CharField(max_length=50, null=True, blank=True)
    player_max = models.IntegerField()
    payment_plan = models.CharField(max_length=20, choices=[('team whole', 'team whole'),
        ('team per person', 'team per person'),
        ('individual', 'individual'),
        ])
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __str__(self):
        return self.name

class TeamMember(models.Model):

    user = models.ForeignKey(AusomeUser, on_delete=models.CASCADE) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE) 
    is_captain = models.BooleanField(default=False) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __str__(self):
        return self.user.first_name

class PendingTeamMember(models.Model):

    user = models.ForeignKey(AusomeUser, on_delete=models.CASCADE) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __str__(self):
        return self.user.first_name

class Game(models.Model):

    league = models.ForeignKey(League, on_delete=models.CASCADE) 
    teams = models.ManyToManyField(Team) 
    date = models.DateTimeField() 
    location = models.TextField() 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __str__(self):
        return 'Game - ' + str(self.pk)

class Win(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE) 
    game = models.ForeignKey(Game, on_delete=models.CASCADE) 
    score = models.CharField(max_length=50) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __str__(self):
        return 'Win - ' + str(self.pk)

class Loss(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE) 
    game = models.ForeignKey(Game, on_delete=models.CASCADE) 
    score = models.CharField(max_length=50) 
    date_added = models.DateTimeField(auto_now_add=True) 

    def natural_key(self):
        pass

    def __str__(self):
        return 'Loss - ' + str(self.pk)
