from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from . import models, decorators

# Create your views here.
def index(request):
    return render(request, 'ausome_sports/index.html')

@decorators.login_required
def get_user_profile(request):
    profile_set = models.AusomeUser.objects.filter(user=request.user)
    #data = serializers.serialize('json', profile_set, fields=('first_name', 'last_name'))

    return JsonResponse(data=profile_set, safe=False)
