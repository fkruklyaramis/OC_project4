from models.round_model import Round


class RoundView():
    """RoundView class represents the view layer for handling Round display in a tournament.

    The class manages the presentation aspects of a Round object, providing methods
    to display round-related information to users.

    Attributes:
        round (Round): A Round instance that this view represents and displays.

    Example:
        round_instance = Round()
        round_view = RoundView(round_instance)
        round_view.start_round()
    """

    def __init__(self, round: Round):
        self.round = round

    def start_round(self):
        print(f"\nRound {self.round.number} started")

    def display_round_matches(self, players: list):
        """
        Display the matches for the current round.
        Args:
            players (list): List of paired players where consecutive pairs will play against each other
        """
        print("\nMatches for this round:")
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1]
            print(f"Match {(i//2) + 1}: {player1.first_name} {player1.last_name} vs "
                  f"{player2.first_name} {player2.last_name}")
