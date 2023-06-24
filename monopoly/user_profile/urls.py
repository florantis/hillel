from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("top_players/", views.top_players, name="top_players"),
    path("recent_games/", views.recent_games, name="recent_games"),

    path("user/<int:id>/", views.view_user_page, name="user_page"),
    path("user/<int:id>/won_games/", views.user_won_games, name="user_page"),
    
    path("user/<int:id>/trophies/", views.view_trophies, name="user_page"),
    path("user/<int:user_id>/trophies/<int:trophy_id>/", views.view_granted_trophy, name="user_page"),

    path("game/<int:id>/", views.view_game_info, name="game_info"),
]