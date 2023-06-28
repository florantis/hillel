from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=24)
    user_bio = models.CharField(max_length=512)
    experience = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()

    def __str__(self):
        return self.username
    

class Game(models.Model):
    time_when_started = models.TimeField()
    number_of_turns = models.IntegerField()
    # Did game end early? (e.g if everyone left)
    ended_early = models.BooleanField()
    winner = models.ForeignKey("User", on_delete=models.CASCADE)


class GrantedTrophy(models.Model):
    type = models.ForeignKey("Trophy", on_delete=models.CASCADE)
    time_when_recieved = models.TimeField()
    owner = models.ForeignKey("User", on_delete=models.CASCADE)

class Trophy(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.title