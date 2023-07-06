from django.db import models

# Create your models here.


class Profile(models.Model):
    """Fields: auth_user, username, user_bio, experience, wins, losses"""
    auth_user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    # username = models.CharField(max_length=24)
    user_bio = models.CharField(max_length=512)
    experience = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()

    def __str__(self):
        return self.auth_user.username


class Commentary(models.Model):
    """Fields: owner, on_page, content, time"""
    owner = models.ForeignKey("auth.user", on_delete=models.CASCADE, related_name="owner")
    on_page = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    time = models.TimeField(auto_now_add=True)


class Game(models.Model):
    time_when_started = models.TimeField()
    number_of_turns = models.IntegerField()
    # Did game end early? (e.g if everyone left)
    ended_early = models.BooleanField()
    winner = models.ForeignKey("auth.user", on_delete=models.CASCADE)


class GrantedTrophy(models.Model):
    type = models.ForeignKey("Trophy", on_delete=models.CASCADE)
    time_when_recieved = models.TimeField()
    owner = models.ForeignKey("auth.user", on_delete=models.CASCADE)


class Trophy(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    assignee = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True)
    title = models.CharField(max_length=32)
    message = models.CharField(max_length=512)
    time_when_posted = models.TimeField(auto_now_add=True)
    is_open = models.BooleanField(auto_created=True)
