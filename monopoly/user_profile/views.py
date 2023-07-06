from django.http import Http404
from django.shortcuts import redirect, render
# from django.http import HttpResponse
from django.urls import reverse
from .models import Profile, Game, GrantedTrophy, Trophy, Commentary, SupportTicket
from .forms import CommentaryForm, RegisterForm, SupportTicketForm
from django.views.generic import FormView, DetailView
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate, login as login_user, logout as logout_user


# Create your views here.
def index(request):
    return render(request, "user_profile/index.html", {})


def top_players(request):
    user_list = list(Profile.objects.all())
    user_list.sort(reverse=True, key=lambda user: user.experience)
    return render(request, "user_profile/top_users.html",
                  {"user_list": user_list})


def recent_games(request):
    game_list = list(Game.objects.all())[-5:]
    game_list.sort(reverse=True, key=lambda game: game.time_when_started)
    return render(request, "user_profile/recent_games.html", {"game_list": game_list})


def view_user_page(request, id):
    player = Profile.objects.get(pk=id)
    comment_list = list(Commentary.objects.filter(on_page=id))
    comment_list.sort(reverse=True, key=lambda game: game.time)
    won_games_count = len(Game.objects.filter(winner=player.auth_user))
    return render(request, "user_profile/user_page.html", {"user": player, "comment_list": comment_list,
                                                           "won_games_count": won_games_count})


def view_game_info(request, id):
    game = Game.objects.get(pk=id)
    return render(request, "user_profile/game_info.html", {"game": game})


def user_won_games(request, id):
    user = AuthUser.objects.get(pk=id)
    game_list = Game.objects.filter(winner=user)
    return render(request, "user_profile/user_won_games.html", {"game_list": game_list, "user": user})

def edit_user_bio(request, id):
    context = {}
    if request.user.pk != id:
        raise Http404

    if request.POST:
        user = Profile.objects.get(pk=id)
        user.user_bio = request.POST.get("bio")
        user.save()
        context["success"] = True
    
    return render(request, "user_profile\edit_user_bio.html", context)


def view_trophies(request, id):
    user = Profile.objects.get(pk=id)
    trophy_list = GrantedTrophy.objects.filter(owner=user.auth_user)
    return render(request, "user_profile/user_trophies.html", {"user": user, "trophy_list": trophy_list})


def view_granted_trophy(request, user_id, trophy_id):
    user = Profile.objects.get(pk=user_id)
    trophy_type = Trophy.objects.get(pk=trophy_id)
    granted_trophy = GrantedTrophy.objects.get(owner=user.auth_user, type=trophy_type)
    return render(request, r"user_profile\trophy.html", {"user": user, "trophy": granted_trophy})


def success_comment(request, id):
    owner = request.user
    on_page = AuthUser.objects.get(pk=id)
    form_data = CommentaryForm(request.POST)

    if form_data.is_valid():
        comment = Commentary.objects.create(owner=owner, on_page=on_page, content=request.POST.get("comment"))
    else:
        comment = None

    return render(request, "user_profile/commentary_created.html", {"comment": comment,
                                                                    "error_list": form_data.errors,
                                                                    "id": id})


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


def register(request):
    context = {}
    if request.POST:
        form_data = RegisterForm(request.POST)
        context["errors"] = form_data.errors
        if form_data.is_valid():
            new_user = AuthUser.objects.create_user(username=form_data.cleaned_data['username'],
                                                    password=form_data.cleaned_data['password'])

            new_user.save()

            Profile.objects.create(auth_user=new_user, user_bio='', experience=0, wins=0, losses=0)

            login_user(request, new_user)
            context["user"] = new_user
    return render(request, 'user_profile/register.html', context)


def login(request):
    context = {}
    if request.POST:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user:
            login_user(request, user)
            context["user"] = user
        else:
            context["errors"] = 'Wrong login or password!'


    return render(request, 'user_profile/login.html', context)


def logout(request):
    context = {}
    if request.user.is_authenticated:
        if request.POST:
            if request.POST.get("confirm") == "True":
                logout_user(request)
                context["success"] = True
            else:
                return redirect(reverse("index"))
        else:
            pass
        
    else:
        context['is_anon'] = True

    return render(request, "user_profile/logout.html", context)