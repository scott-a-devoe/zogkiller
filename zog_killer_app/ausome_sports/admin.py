from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.AusomeUser)
admin.site.register(models.League)
admin.site.register(models.Team)
admin.site.register(models.TeamMember)
admin.site.register(models.PendingTeamMember)
admin.site.register(models.Game)
admin.site.register(models.Win)
admin.site.register(models.Loss)
