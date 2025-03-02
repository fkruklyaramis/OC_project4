from views.report_view import ReportView
from views.player_view import PlayerView
from controllers.player_controller import PlayerController
from models.data_manager import DataManager


class ReportController(DataManager):

    def __init__(self, view: ReportView):
        super().__init__()
        self.view = view
        self.player_controller = PlayerController(PlayerView())
        self.menu_choice_list = [
            {'value': 1, 'label': 'Show all players (alphabetically)', 'callback':
             self.show_all_players},
            {'value': 2, 'label': 'Show all tournaments', 'callback':
             self.show_all_tournaments},
            {'value': 3, 'label': 'Show tournament details by tournament name', 'callback':
             self.show_tournament_by_location},
            {'value': 4, 'label': 'Show tournament players by tournament name', 'callback':
             self.show_tournament_players},
            {'value': 5, 'label': 'Show tournament rounds and matches by tournament name', 'callback':
             self.show_tournament_rounds},
            {'value': 6, 'label': 'Back to main menu', 'callback': None}
        ]

        self.view.set_choice_list(self.menu_choice_list)

    def manage_reports(self):
        """
        Manages the report menu interactions and executes corresponding callbacks.
        This method displays a menu through the view, processes the user's choice,
        and executes the corresponding callback function if one exists for the selected option.
        Returns:
            None: The method doesn't return any value but executes the selected callback function.
        """

        choice = self.view.menu()
        menu_choice = next((item for item in self.menu_choice_list if item['value'] == choice), None)
        if menu_choice and menu_choice['callback'] is not None:
            menu_choice['callback']()

    def show_all_players(self):
        """
        Display all players sorted by last name and first name.
        This method retrieves all players from storage, sorts them alphabetically
        by last name (and first name for players with same last name),
        then displays the sorted list using the view.
        Returns:
            None
        """

        players = self.load_players()
        sorted_players = sorted(players, key=lambda x: (x['last_name'].lower(), x['first_name'].lower()))
        self.view.show_players_list(sorted_players)

    def show_all_tournaments(self):
        """
        Display all tournaments sorted by start date.

        This method retrieves all tournaments from storage, sorts them by start date,
        and displays them using the view component.

        Returns:
            None
        """

        tournaments = self.load_tournaments()
        sorted_tournaments = sorted(tournaments, key=lambda x: x['startDate'])
        self.view.show_all_tournaments(sorted_tournaments)

    def show_tournament_by_location(self):
        """
        Display details of a tournament based on its location.
        This method prompts the user for a location, searches for a tournament in that location,
        and displays its details if found.
        Returns:
        Notes:
            - Calls view.get_tournament_location() to get location input from user
            - Loads tournaments from storage
            - Uses case-insensitive location matching
            - If tournament is found, displays details via view.show_tournament_details()
            - If no tournament is found, prints error message
            - Returns to report management menu after completion
        """

        name = self.view.get_tournament_name()
        tournaments = self.load_tournaments()
        tournament = next(
            (t for t in tournaments if t['name'].lower() == name.lower()),
            None
        )
        if tournament:
            self.view.show_tournament_details(tournament)
        else:
            self.view.show_tournament_details(None)

    def show_tournament_players(self):
        name = self.view.get_tournament_name()
        tournaments = self.load_tournaments()
        tournament = next(
            (t for t in tournaments if t['name'].lower() == name.lower()),
            None
        )

        if tournament:
            players = tournament['playerList']
            sorted_players = sorted(
                players,
                key=lambda x: (x['last_name'].lower(), x['first_name'].lower())
            )
            self.view.show_tournament_players(sorted_players, tournament['name'])
        else:
            self.view.show_tournament_rounds(None, None)

    def show_tournament_rounds(self):
        """Display rounds and matches of a tournament"""
        name = self.view.get_tournament_name()
        tournaments = self.load_tournaments()
        tournament = next(
            (t for t in tournaments if t['name'].lower() == name.lower()),
            None
        )
        if tournament:
            self.view.show_tournament_rounds(tournament['roundList'], tournament['name'])
        else:
            self.view.show_tournament_rounds(None, None)
