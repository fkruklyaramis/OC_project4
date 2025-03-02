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
