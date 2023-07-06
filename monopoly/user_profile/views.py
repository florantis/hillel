from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .models import User, Game, GrantedTrophy, Trophy, Commentary, SupportTicket
from .forms import CommentaryForm, SupportTicketForm
from django.views.generic import FormView, DetailView

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
    comment_list = list(Commentary.objects.filter(on_page=id))
    comment_list.sort(reverse=True, key=lambda game: game.time)
    return render(request, "user_profile/user_page.html", {"user": player, "comment_list": comment_list})


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
    return render(request, r"user_profile\trophy.html", {"user": user, "trophy": granted_trophy})


def success_comment(request, id):
    owner = User.objects.get(pk=1)
    on_page = User.objects.get(pk=id)
    form_data = CommentaryForm(request.POST)

    if form_data.is_valid():
        comment = Commentary.objects.create(owner=owner, on_page=on_page, content=request.POST.get("comment"))
    else:
        comment = None

    return render(request, "user_profile/commentary_created.html", {"comment": comment, "error_list": form_data.errors, "id": id})


class SupportPage(FormView):
    form_class = SupportTicketForm
    template_name = "user_profile/support_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_list"] = SupportTicket.objects.filter(is_open=True)

        return context
    
    def form_valid(self, form):
        SupportTicket.objects.create(assignee=form.cleaned_data["assignee"], email=form.cleaned_data["email"],
                                     message=form.cleaned_data["message"], title=form.cleaned_data["title"],
                                     is_open=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("support_page")

    
class SupportTicketDetail(DetailView):
    model = SupportTicket
    
    


