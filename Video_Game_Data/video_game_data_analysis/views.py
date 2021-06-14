from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
import json

# Create your views here.


def index(request):

    all_games = requests.get('https://api.dccresource.com/api/games/').json()

    platform_dict = {}
    for game in all_games:
        if isinstance(game['year'], int) and game['year'] >= 2013:
            if game['platform'] not in platform_dict:
                platform_dict[game['platform']] = game['globalSales']
            elif game['platform'] in platform_dict:
                platform_dict[game['platform']] += game['globalSales']

    platforms_list = []
    copies_per_platform = []
    for platform, copies in platform_dict.items():
        platforms_list.append(platform)
        copies_per_platform.append(copies)

    context = {
               'all_games': all_games,
               'all_platforms': platforms_list,
               'copies': copies_per_platform}
    return render(request, 'index.html', context)


def search_by_title(request):
    if request.method == 'GET':
        context = {'get': True}
        return render(request, 'search_by_title.html', context)
    elif request.method == 'POST':
        search = request.POST.get('title')
        alphanumeric_search = [character for character in search if character.isalnum()]
        search = "".join(alphanumeric_search)
        all_games = requests.get('https://api.dccresource.com/api/games/').json()
        found_game = None
        for game in all_games:
            alphanumeric = [character for character in game['name'] if character.isalnum()]
            alphanumeric_game = "".join(alphanumeric)
            if alphanumeric_game.upper() == search.upper():
                if found_game is not None:
                    found_game.append(game)
                else:
                    found_game = [game]
        if found_game is not None:
            platforms = []
            sales = []
            for entry in found_game:
                platforms.append(entry['platform'])
                sales.append(entry['globalSales'])
            context = {'game': found_game,
                       'platforms': platforms,
                       'sales': sales}
        else:
            context = {'game': None}
        return render(request, 'search_by_title.html', context)


def compare_platforms(request):
    years = []
    i = 1980
    while i <= 2021:
        years.append(i)
        i += 1
    if request.method == "GET":
        context = {'years': years}
    else:
        chosen_year = request.POST.get('year')
        all_games = requests.get('https://api.dccresource.com/api/games/').json()
        games_in_year = []
        for entry in all_games:
            if str(entry['year']) == chosen_year:
                games_in_year.append(entry)
        platform_releases = {}
        for entry in games_in_year:
            if entry['platform'] not in platform_releases:
                platform_releases[entry['platform']] = 1
            else:
                platform_releases[entry['platform']] += 1
        ## Splitting platform_releases dict into two lists in order to comply with Chart.js parameters:
        platforms = []
        releases = []
        for key in platform_releases:
            platforms.append(key)
            releases.append(platform_releases[key])
        context = {'years': years,
                   'year': chosen_year,
                   'platforms': platforms,
                   'releases': releases,
                   'chart_data': True}
    return render(request, 'compare_platforms.html', context)


def compare_publishers(request):
    all_games = requests.get('https://api.dccresource.com/api/games/').json()
    platforms = []
    for entry in all_games:
        if entry['platform'] not in platforms:
            platforms.append(entry['platform'])
    if request.method == "GET":
        context = {'platforms': platforms}
    else:
        platform = request.POST.get('platform')
        publisher_sales = {}
        for game in all_games:
            if game['platform'] == platform:
                if game['publisher'] not in publisher_sales:
                    publisher_sales[game['publisher']] = game['globalSales']
                else:
                    publisher_sales[game['publisher']] += game['globalSales']
        big_publishers = []
        big_sales = []
        little_publishers = []
        little_sales = []
        for publisher in publisher_sales:
            if publisher_sales[publisher] > 5:
                big_publishers.append(publisher)
                big_sales.append(publisher_sales[publisher])
            else:
                little_publishers.append(publisher)
                little_sales.append(publisher_sales[publisher])
        context = {'platforms': platforms,
                   'big_publishers': big_publishers,
                   'big_sales': big_sales,
                   'little_publishers': little_publishers,
                   'little_sales': little_sales,
                   'chart_data': True}
    return render(request, 'compare_publishers.html', context)

