from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
import json

# Create your views here.


def index(request):

    all_games = requests.get('https://api.dccresource.com/api/games/').json()
    ##^returns a LIST of dictionaries (converted from json)

    game = all_games[1]

    platform_dict = {}
    for game in all_games:
        if game['platform'] not in platform_dict:
            platform_dict[game['platform']] = game['globalSales']
        elif game['platform'] in platform_dict:
            platform_dict[game['platform']] += game['globalSales']

    platforms_list = []
    copies_per_platform = []
    for platform, copies in platform_dict.items():
        platforms_list.append(platform)
        copies_per_platform.append(copies)

    helper_message = requests.get('https://api.dccresource.com/')
    helper_message = helper_message.json()

    context = {'message': helper_message,
               'game': game,
               'all_games': all_games,
               'all_platforms': platforms_list,
               'copies': copies_per_platform}
    return render(request, 'index.html', context)


def search_by_title(request):
    if request.method == 'GET':
        return render(request, 'search_by_title.html')
    elif request.method == 'POST':
        search = request.POST.get('title')
        all_games = requests.get('https://api.dccresource.com/api/games/').json()
        found_game = 'none found'
        for game in all_games:
            if game['name'].upper() == search.upper():
                found_game = game
        context = {'game': found_game}
        return render(request, 'search_by_title.html', context)
