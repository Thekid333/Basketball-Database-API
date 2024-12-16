import json
import os
from app.models import Team, Player, Game, Stats, Shot
from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Loads data from raw_data files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data load...")
        load_data()  # Call your existing function
        self.stdout.write("Data load completed.")


@transaction.atomic
def load_data():
    # Loads teams
    with open(os.path.join(settings.BASE_DIR, 'raw_data/teams.json')) as f:
        teams_data = json.load(f)
        for team in teams_data:
            Team.objects.get_or_create(team_id=team['id'], team_name=team['name'])

    # Load players without assigning team first
    with open(os.path.join(settings.BASE_DIR, 'raw_data/players.json')) as f:
        players_data = json.load(f)
        for player in players_data:
            Player.objects.get_or_create(player_id=player['id'], player_name=player['name'], team=None)

    # Load games and associate players with teams based on games
    with open(os.path.join(settings.BASE_DIR, 'raw_data/games.json')) as f:
        games_data = json.load(f)
        for game in games_data:
            home_team = Team.objects.get(team_id=game['homeTeam']['id'])
            away_team = Team.objects.get(team_id=game['awayTeam']['id'])

            # Assign players to home or away team based on their participation
            for stat in game['homeTeam']['players']:
                player = Player.objects.get(player_id=stat['id'])
                player.team = home_team
                player.save()

            for stat in game['awayTeam']['players']:
                player = Player.objects.get(player_id=stat['id'])
                player.team = away_team
                player.save()

    # Now, create the Game, Stats, and Shot entries
    for game in games_data:
        home_team = Team.objects.get(team_id=game['homeTeam']['id'])
        away_team = Team.objects.get(team_id=game['awayTeam']['id'])
        game_instance, created = Game.objects.get_or_create(
            game_id=game['id'],
            game_date=game['date'],
            home_team=home_team,  # No need for _id, Django handles it
            away_team=away_team   # No need for _id, Django handles it
        )

        # Add player stats and shots for home and away team
        for team in ['homeTeam', 'awayTeam']:
            current_team = game[team]
            for stat in current_team['players']:
                player = Player.objects.get(player_id=stat['id'])
                stat_instance = Stats.objects.create(
                    player=player,
                    game=game_instance,
                    is_starter=stat['isStarter'],
                    minutes=stat['minutes'],
                    points=stat['points'],
                    assists=stat['assists'],
                    offensive_rebounds=stat['offensiveRebounds'],
                    defensive_rebounds=stat['defensiveRebounds'],
                    steals=stat['steals'],
                    blocks=stat['blocks'],
                    turnovers=stat['turnovers'],
                    defensive_fouls=stat['defensiveFouls'],
                    offensive_fouls=stat['offensiveFouls'],
                    free_throws_made=stat['freeThrowsMade'],
                    free_throws_attempted=stat['freeThrowsAttempted'],
                    two_pointers_made=stat['twoPointersMade'],
                    two_pointers_attempted=stat['twoPointersAttempted'],
                    three_pointers_made=stat['threePointersMade'],
                    three_pointers_attempted=stat['threePointersAttempted']
                )

                # Add shots for each player
                for shot in stat.get('shots', []):
                    Shot.objects.create(
                        player=player,
                        stat=stat_instance,
                        is_make=shot['isMake'],
                        location_x=shot['locationX'],
                        location_y=shot['locationY']
                    )

def run():
    load_data()
