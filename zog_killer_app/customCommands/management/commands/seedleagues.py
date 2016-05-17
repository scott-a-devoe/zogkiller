from django.core.management import BaseCommand
from django.utils import dateparse
from ausome_sports import models

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Seeds database with leagues"
    
    # A command must define handle()
    def handle(self, *args, **options):
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
        league.status = 'open'
        league.team_max = 10

        league.save()
