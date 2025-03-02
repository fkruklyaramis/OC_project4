from views.round_view import RoundView
from models.round_model import Round
from models.tournament_model import Tournament
from models.player_model import Player
from controllers.match_controller import MatchController
from datetime import datetime
import random


class RoundController:

    def __init__(self, tournament: Tournament, round_number: int):
        self.tournament = tournament
        self.round = Round(number=round_number)
        self.round.name = f"Round {round_number}"
        self.view = RoundView(self.round)
        self.tournament = tournament

    def manage_round(self):
        """
        Manage a round of a tournament.
        This method is responsible for starting matches between paired players for a round.
        Returns:
            dict: A dictionary with round details and match results
        Format example:
            {
                "name": "Round 1",
                "startDate": "2021-01-01 10:00:00",
                "endDate": "2021-01-01 10:30:00",
                "matchList": [
                    {
                        "match": [
                            [{"chess_id": "AB12345", "score": 1.0}, ...],
                            [{"chess_id": "CD67890", "score": 0.0}, ...]
                        ]
                    },
                    ...
                ]
            }
        Notes:
            - The round start and end dates are set automatically
            - Players are paired based on the Swiss tournament system
            - Match results are stored in the round object
        """
        self.view.start_round()
        players = []
        if self.round.number == 1:
            # randomize players for firdst round
            random.shuffle(self.tournament.playerList)
            players = self.tournament.playerList
            # afficher la liste des matchs du premier round
        else:
            # call matching player method
            players = self.pair_players()
        self.start_matches(players)
        self.round.endDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.round.model_dump()

    def start_matches(self, players: list):
        """
        Start matches between paired players for a round.
        Args:
            players (list): A list of paired players in order [player1, player2, player3, player4, ...],
                            where consecutive pairs of players will play against each other.
        """

        match_count = self.match_count()

        # players are paired two by two, getting the first and second player
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1]

            match = self.new_match(player1, player2)
            result = match.play_match((i//2) + 1, match_count)
            self.round.matchList.append(result)

    def new_match(self, player1: Player, player2: Player) -> MatchController:
        """
        Create a new match instance for two players.
        Args:
            player1 (Player): First player
            player2 (Player): Second player
        Returns:
            MatchController: A new match controller instance
        """
        match_controller = MatchController(self.tournament, player1, player2)
        return match_controller

    def match_count(self) -> int:
        """
        Calculate the number of matches to be played in a round.
        Returns:
            int: Number of matches to be played
        """
        return int((len(self.tournament.playerList) + 1) / 2)

    def pair_players(self):
        """
        Pairs players for a tournament round using Swiss tournament system.
        The pairing is done based on the following rules:
        1. Players are sorted by their current tournament scores
        2. Players who have not played against each other are paired
        3. In case of equal scores, random factor is used for ranking
        Returns:
            list: A list of paired players in order [player1, player2, player3, player4, ...],
                  where consecutive pairs of players will play against each other.
        Note:
            - Players cannot be paired with someone they've already played against
            - Each player appears exactly once in the returned list
            - If a perfect pairing cannot be achieved (due to previous matches or odd number of players),
              some players might remain unpaired
        """

        player_scores = self.calculate_player_scores()

        # ranking players by score
        sorted_players = sorted(
            self.tournament.playerList,
            key=lambda p: (player_scores.get(p.chess_id, 0), random.random()),
            reverse=True
        )

        # create pairs of players that have not played together
        paired_players = []
        used_players_ids = set()

        for player1 in sorted_players:
            if player1.chess_id in used_players_ids:
                continue

            # search for a player to pair with player1
            for player2 in sorted_players:
                if (player2.chess_id not in used_players_ids and player1.chess_id != player2.chess_id
                   and not self.have_played_together(player1, player2)):

                    paired_players.extend([player1, player2])
                    used_players_ids.add(player1.chess_id)
                    used_players_ids.add(player2.chess_id)
                    break

        return paired_players

    def have_played_together(self, player1: Player, player2: Player) -> bool:
        """
        Check if two players have already played together in any round of the tournament.
        Args:
            player1 (Player): First player to check
            player2 (Player): Second player to check
        Returns:
            bool: True if players have played together, False otherwise
        Notes:
            - Checks all rounds in the tournament's roundList
            - Compares chess_ids of players in each match
            - Match order doesn't matter (player1 vs player2 or player2 vs player1)
        """

        for round_data in self.tournament.roundList:
            for match in round_data.get('matchList', []):
                match_data = match.get('match', [])
                p1 = match_data[0][0]
                p2 = match_data[1][0]

                if ((p1.chess_id == player1.chess_id and p2.chess_id == player2.chess_id) or (
                     p1.chess_id == player2.chess_id and p2.chess_id == player1.chess_id)):
                    return True
        return False

    def calculate_player_scores(self) -> dict:
        """
        Calculate the total scores for each player based on all rounds played in the tournament.
        Returns:
            dict: A dictionary with player chess IDs as keys and their cumulative scores as values.
                    If no rounds have been played, returns an empty dictionary.
        Format example:
            {
                "AB12345": 2.5,  # Where "AB12345" is the chess_id and 2.5 is the total score
                "CD67890": 1.0
            }
        Note:
            - Scores are accumulated from all matches in all rounds
            - Each player's score is initialized to 0 if they haven't played before
            - Players are identified by their chess_id
        """

        player_scores = {}
        if not self.tournament.roundList:
            return player_scores

        for round_data in self.tournament.roundList:
            for match in round_data.get('matchList', []):
                match_data = match.get('match', [])

                player1 = match_data[0][0]
                score1 = match_data[0][1]
                player2 = match_data[1][0]
                score2 = match_data[1][1]

                player_scores[player1.chess_id] = player_scores.get(player1.chess_id, 0) + score1
                player_scores[player2.chess_id] = player_scores.get(player2.chess_id, 0) + score2

        return player_scores
