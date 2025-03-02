from models.tournament_model import Tournament
from models.data_manager import DataManager
from views.tournament_view import TournamentView
from views.player_view import PlayerView
from views.report_view import ReportView
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from controllers.report_controller import ReportController
from utils.validators import validate_date_format, validate_tournament_start_date, validate_tournament_dates_order


class TournamentController(DataManager):
    """
    Controller class for managing tournament operations.

    This class handles the creation, management, and execution of chess tournaments.
    It provides functionality for adding tournaments, managing players, viewing reports,
    and orchestrating tournament rounds.

    Attributes:
        view (TournamentView): The view instance for tournament-related UI
        tournaments_file (str): Path to the JSON file storing tournament data
        menu_choice_list (list): List of menu options and their callbacks
        current_tournament (Tournament): Currently active tournament instance
    """
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
        Creates a new tournament by collecting necessary information from the user.
        This method handles the creation of a new tournament by:
        1. Getting tournament details (name, location, dates) from user input
        2. Validating date formats and logical constraints
        3. Loading and selecting players for the tournament
        4. Creating tournament rounds
        5. Saving the tournament data
        Returns:
            None
        Side Effects:
            - Updates self.current_tournament with the new tournament
            - Saves tournament data to storage
            - Displays messages to user through view
            - Creates and initializes tournament rounds
        Raises:
            May raise exceptions from validate_date_format(), validate_tournament_start_date(),
            validate_tournament_dates_order() if date validation fails
        """

        print("\nCreate tournament")
        tournament_name = self.view.get_name()
        tournament_location = self.view.get_location()

        while True:
            start_date = self.view.get_start_date()
            if not validate_date_format(start_date):
                self.view.show_message("Invalid date format. Please use YYYY-MM-DD format.")
                continue
            if not validate_tournament_start_date(start_date):
                self.view.show_message("Tournament cannot start in the past.")
                continue
            break

        while True:
            end_date = self.view.get_end_date()
            if not validate_date_format(end_date):
                self.view.show_message("Invalid date format. Please use YYYY-MM-DD format.")
                continue
            if not validate_tournament_dates_order(start_date, end_date):
                self.view.show_message("End date must be after start date.")
                continue
            break

        players = PlayerController(PlayerView()).load_data('players')
        self.view.set_players_list(players)
        player_list = self.view.select_players()
        description = self.view.get_description()

        tournament_data = {
            "name": tournament_name,
            "location": tournament_location,
            "startDate": start_date,
            "endDate": end_date,
            "playerList": player_list,
            "description": description
        }

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
            round_data, is_last_round = round_controller.manage_round()
            rounds.append(round_data)
            self.current_tournament.playerList = players
            if is_last_round:
                self.end_tournament()
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

        self.save_data(tournament_dict, 'tournaments')

    def end_tournament(self):
        """
        End the tournament, determine winner(s) and display results.
        Handles single winner and tie cases.
        """
        if not self.current_tournament:
            self.view.show_message("No active tournament")
            return

        players = self.current_tournament.playerList
        if not players:
            self.view.show_message("No players in tournament")
            return

        # Find highest score and winners
        max_points = max(player.point for player in players)
        winners = [p for p in players if p.point == max_points]

        # Display results through view
        if len(winners) > 1:
            self.view.display_tie(winners, max_points)
        else:
            self.view.display_single_winner(winners[0])

        self.saving_tournament(self.current_tournament)
