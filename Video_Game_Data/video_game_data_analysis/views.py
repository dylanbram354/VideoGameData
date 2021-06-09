from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
import json

# Create your views here.


def index(request):
    response = requests.get('https://api.dccresource.com/api/games/5faac562db090e1a5c2dea2d')
    game = response.json()
    context = {'game': game}
    return render(request, 'index.html', context)