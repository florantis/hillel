from django.contrib import admin
from .models import User, Game, GrantedTrophy, Trophy, Commentary, SupportTicket
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "experience", "wins", "losses")

class GameAdmin(admin.ModelAdmin):
    list_display = ("pk", "time_when_started", "number_of_turns", "ended_early",)

class GrantedTrophyAdmin(admin.ModelAdmin):
    list_display = ("type", "time_when_recieved", "owner")

class TrophyAdmin(admin.ModelAdmin):
    list_display = ("title", "description")

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ("owner", "content")

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("assignee", "title")


admin.site.register(User, UserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Trophy, TrophyAdmin)
admin.site.register(GrantedTrophy, GrantedTrophyAdmin)
admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(SupportTicket, SupportTicketAdmin)
