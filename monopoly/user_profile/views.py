from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Game, GrantedTrophy, Trophy

# Create your views here.
def index(request):
    return render(request, "user_profile/index.html", {})

def top_players(request):
    user_list = list(User.objects.all())
    user_list.sort(reverse=True, key=lambda user: user.experience)
    
    return render(request, "user_profile/top_users.html", \
                  {"user_list": user_list})

def recent_games(request):
    game_list = list(Game.objects.all())[-5:]
    game_list.sort(reverse=True, key=lambda game: game.time_when_started)
    return render(request, "user_profile/recent_games.html", {"game_list": game_list})

def view_user_page(request, id):
    player = User.objects.get(pk=id)
    return render(request, "user_profile/user_page.html", {"user": player})

def view_game_info(request, id):
    game = Game.objects.get(pk=id)
    return render(request, "user_profile/game_info.html", {"game": game})

def user_won_games(request, id):
    user = User.objects.get(pk=id)
    game_list = Game.objects.filter(winner=user)
    return render(request, "user_profile/user_won_games.html", {"game_list": game_list, "user": user})

def view_trophies(request, id):
    user = User.objects.get(pk=id)
    trophy_list = GrantedTrophy.objects.filter(owner=user)
    return render(request, "user_profile/user_trophies.html", {"user": user, "trophy_list": trophy_list})

def view_granted_trophy(request, user_id, trophy_id):
    user = User.objects.get(pk=user_id)
    trophy_type = Trophy.objects.get(pk=trophy_id)
    granted_trophy = GrantedTrophy.objects.get(owner=user, type=trophy_type)
    print(granted_trophy)
    return render(request, r"user_profile\trophy.html", {"user": user, "trophy": granted_trophy})
