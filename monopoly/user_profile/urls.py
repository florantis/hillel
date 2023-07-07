from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("top_players/", views.top_players, name="top_players"),
    path("recent_games/", views.recent_games, name="recent_games"),

    path("support/", views.SupportPage.as_view(), name="support_page"),
    path("support/ticket_info/<pk>/", views.SupportTicketDetail.as_view(), name="support_ticket_info"),

    path("user/<int:id>/", views.view_user_page, name="user_page"),
    path("user/<int:id>/won_games/", views.user_won_games, name="user_won_games"),
    path("user/<int:id>/edit/bio/", views.edit_user_bio, name='edit_bio'),

    path("user/<int:id>/trophies/", views.view_trophies, name="user_trophies"),
    path("user/<int:user_id>/trophies/<int:trophy_id>/", views.view_granted_trophy, name="user_trophy"),

    path("user/<int:id>/comment_info/", views.success_comment, name="user_comment_success"),

    path("game/<int:id>/", views.view_game_info, name="game_info"),

    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout")
]
