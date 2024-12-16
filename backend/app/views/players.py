from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Player, Stats, Shot, Team

class PlayerSummary(APIView):

    def get(self, request, player_id):
        # Fetch the player
        try:
            player = Player.objects.select_related('team').get(player_id=player_id)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=404)

        # Fetch the player's game statistics
        stats = Stats.objects.filter(player=player).select_related('game')
        
        games_data = []
        for stat in stats:
            # Fetch related shots for this stat
            shots = Shot.objects.filter(stat=stat)
            shots_data = [
                {
                    "isMake": shot.is_make,
                    "locationX": shot.location_x,
                    "locationY": shot.location_y
                } for shot in shots
            ]
            
            # Construct game data including shots
            game_data = {
                "date": stat.game.game_date,
                "isStarter": stat.is_starter,
                "minutes": stat.minutes,
                "points": stat.points,
                "assists": stat.assists,
                "offensiveRebounds": stat.offensive_rebounds,
                "defensiveRebounds": stat.defensive_rebounds,
                "steals": stat.steals,
                "blocks": stat.blocks,
                "turnovers": stat.turnovers,
                "defensiveFouls": stat.defensive_fouls,
                "offensiveFouls": stat.offensive_fouls,
                "freeThrowsMade": stat.free_throws_made,
                "freeThrowsAttempted": stat.free_throws_attempted,
                "twoPointersMade": stat.two_pointers_made,
                "twoPointersAttempted": stat.two_pointers_attempted,
                "threePointersMade": stat.three_pointers_made,
                "threePointersAttempted": stat.three_pointers_attempted,
                "shots": shots_data  # Include the shots data here
            }
            games_data.append(game_data)

        # Get the player's team name
        team_name = player.team.team_name if player.team else None

        # Construct the response in the required format
        response_data = {
            "name": player.player_name,
            "team": team_name,  # Include the team name here
            "games": games_data
        }

        return Response(response_data)
