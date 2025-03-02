from models.tournament_model import Tournament
from models.data_manager import DataManager
from views.tournament_view import TournamentView
from views.player_view import PlayerView
from views.report_view import ReportView
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from controllers.report_controller import ReportController


class TournamentController(DataManager):

    def __init__(self, view: TournamentView):
        super().__init__()
        self.view = view
        self.tournaments_file = "./data/tournaments.json"
        self.menu_choice_list = [{'value': 1, 'label': 'Start a tournament', 'callback': self.add_tournament},
                                 {'value': 2, 'label': 'Manage players', 'callback': self.manage_players},
                                 {'value': 3, 'label': 'View reports', 'callback': self.view_reports},
                                 {'value': 4, 'label': 'Quit', 'callback': exit}]
        self.view.set_choice_list(self.menu_choice_list)
        self.current_tournament = None

    def view_reports(self):
        report_view = ReportView()
        report_controller = ReportController(report_view)
        report_controller.manage_reports()

    def manage_tournament(self):
        """
        Manages tournament operations based on user menu selection.
        This method displays a menu through the view, matches the user's choice with available options,
        and executes the corresponding callback function if one exists.
        Returns:
        Example:
            tournament_controller.manage_tournament()
        """

        choice = self.view.menu()
        menu_choice = next((item for item in self.menu_choice_list if item['value'] == choice), None)
        if menu_choice and 'callback' in menu_choice:
            menu_choice['callback']()
        else:
            None

    def manage_players(self):
        """
        Delegates player management operations to the PlayerController.
        This method acts as a bridge to the player management functionality,
        instantiating a PlayerController with its associated view and calling
        its manage_players method.
        Returns:
            None
        """

        PlayerController(PlayerView()).manage_players()

    def add_tournament(self):
        """
        Create and initialize a new tournament with players and rounds.
        This method performs the following steps:
        1. Loads existing players
        2. Updates the view with the player list
        3. Gets tournament details from user input
        4. Creates a new Tournament instance
        5. Initializes and starts tournament rounds
        6. Saves the tournament data
        Returns:
            None
        Side Effects:
            - Creates and saves a new Tournament instance
            - Updates self.current_tournament with the new tournament
        """

        players = PlayerController(PlayerView()).load_players()
        self.view.set_players_list(players)
        tournament_data = self.view.get_tournament_details()
        self.current_tournament = Tournament(**tournament_data)
        self.current_tournament.roundList = self.start_rounds()
        self.saving_tournament(self.current_tournament)

    def start_rounds(self) -> list:
        """
        Start all rounds of a tournament.
        This method iterates through the number of rounds in the tournament and
        starts each round by calling the RoundController. It then stores the
        round data in a list.
        Returns:
            list: A list of dictionaries containing round details and match results
        Format example:
            [
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
                },
                ...
            ]
        Notes:
            - The round start and end dates are set automatically
            - Players are paired based on the Swiss tournament system
            - Match results are stored in the round object
        """

        rounds = []
        players = self.current_tournament.playerList
        for i in range(1, self.current_tournament.roundNumber + 1):
            round_controller = RoundController(self.current_tournament, i)
            round_data = round_controller.manage_round()
            rounds.append(round_data)
            self.current_tournament.playerList = players
        return rounds

    def saving_tournament(self, tournament):
        """
        Save a tournament to storage by converting it to a dictionary format.

        This method processes a tournament object and converts it into a dictionary format
        suitable for storage, handling nested player objects and match data.

        Args:
            tournament: A Tournament object containing all tournament information including
                       players, rounds, and matches.

        Returns:
            None

        Notes:
            - Converts player objects to dictionaries using model_dump() if available
            - Processes nested match data to ensure proper serialization
            - Uses the data manager's save_tournament method for actual storage
        """

        tournament_dict = tournament.model_dump()

        tournament_dict['playerList'] = [
            player.model_dump() if hasattr(player, 'model_dump') else player
            for player in tournament_dict['playerList']
        ]

        for round_data in tournament_dict.get('roundList', []):
            for match in round_data.get('matchList', []):
                match_data = match.get('match', [])
                if match_data:
                    for i in range(2):  # Process both players in match
                        player = match_data[i][0]
                        match_data[i][0] = player.model_dump() if hasattr(player, 'model_dump') else player

        self.save_tournament(tournament_dict)
