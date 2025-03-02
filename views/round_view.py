from models.round_model import Round


class RoundView():
    def __init__(self, round: Round):
        self.round = round

    def start_round(self):
        print(f"Round {self.round.number} started")
