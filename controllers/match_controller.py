from models.match_model import Match
from models.player_model import Player
from views.match_view import MatchView
import random


class MatchController:
    def __init__(self, tournament, player1: Player, player2: Player):
        self.tournament = tournament
        self.view = MatchView
        self.colors = self.draw_colors()
        self.match = Match(
            match=([player1, 0], [player2, 0])
        )

    def play_match(self, match_number: int, total_matches: int):
        """
        Executes the match play process and updates the match results.
        This method coordinates with the view to get match results and updates
        the match model with the scores. The scores are stored at specific indexes
        in the match data structure.
        Returns:
            dict: A dictionary containing the match data after updating the results
        """

        match_view = self.view(self.match.match, self.colors)
        result = match_view.play_match(match_number, total_matches)
        self.match.match[0][1] = result[0]
        self.match.match[1][1] = result[1]
        return self.match.model_dump()

    def draw_colors(self) -> dict:
        """
        Randomly assign colors to players.
        Returns:
            dict: A dictionary containing the colors assigned to each player
        """

        colors = ['white', 'black']
        random.shuffle(colors)
        return {'player1_color': colors[0], 'player2_color': colors[1]}
