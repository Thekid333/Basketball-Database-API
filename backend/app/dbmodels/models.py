from django.db import models

# Team Model
class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'team'


# Player Model
class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'player'


# Game Model
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_date = models.DateField()
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.DO_NOTHING)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'game'


# Stats Model
class Stats(models.Model):
    stat_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    is_starter = models.BooleanField()
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    defensive_fouls = models.IntegerField()
    offensive_fouls = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    two_pointers_made = models.IntegerField()
    two_pointers_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()

    class Meta:
        db_table = 'stats'


# Shots Model
class Shot(models.Model):
    shot_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    stat = models.ForeignKey(Stats, on_delete=models.DO_NOTHING)
    is_make = models.BooleanField()
    location_x = models.FloatField()
    location_y = models.FloatField()

    class Meta:
        db_table = 'shots'
