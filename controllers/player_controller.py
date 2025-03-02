from models.player_model import Player
from views.player_view import PlayerView
from models.data_manager import DataManager
from utils.validators import validate_date_format, validate_chess_id, validate_player_age


class PlayerController(DataManager):
    """
    PlayerController class manages player-related operations in a chess tournament system.

    This class handles the creation, storage, and display of player information. It provides
    a menu-based interface for managing players and ensures data validation before storage.
    It inherits from DataManager for data persistence operations.

    Attributes:
        view (PlayerView): The view component for user interaction
        players_file (str): Path to the JSON file storing player data
        menu_choice_list (list): List of dictionaries containing menu options and callbacks
    """
    def __init__(self, view: PlayerView):
        super().__init__()
        self.view = view
        self.players_file = "./data/players.json"
        self.menu_choice_list = [{'value': 1, 'label': 'Add a player', 'callback': self.add_player},
                                 {'value': 2, 'label': 'List player', 'callback': self.list_players},
                                 {'value': 3, 'label': 'Back to main menu', 'callback': None}]
        self.view.set_choice_list(self.menu_choice_list)

    def manage_players(self):
        """
        Manages player-related operations through a menu system.
        This method displays a menu to the user through the view component and processes
        the user's choice. It matches the user's selection with predefined menu options
        and executes the corresponding callback function if one exists.
        Returns:
        Notes:
            - The method relies on self.view.menu() to display and get user input
            - Menu choices are stored in self.menu_choice_list
            - Each valid menu choice should have a 'callback' function defined
        """

        choice = self.view.menu()
        menu_choice = next((item for item in self.menu_choice_list if item['value'] == choice), None)
        if menu_choice and menu_choice['callback'] is not None:
            menu_choice['callback']()

    def add_player(self):
        """
        Add a new player to the system with validated information.
        This method collects player information through the view interface and performs validation
        on the input data. It ensures that:
        - Birth date is in correct format (YYYY-MM-DD) and player is at least 18 years old
        - Chess ID follows the required format (two letters followed by five digits)
        The validated player data is then saved to persistent storage.
        Returns:
            None
        Side Effects:
            - Interacts with user through view interface for data input
            - Saves player data to storage system
            - Shows success/error messages through view interface
        """

        last_name = self.view.get_last_name()
        first_name = self.view.get_first_name()

        while True:
            birth_date = self.view.get_birth_date()
            if not validate_date_format(birth_date):
                self.view.show_message("Invalid date format. Please use YYYY-MM-DD format.")
                continue
            if not validate_player_age(birth_date):
                self.view.show_message("Player must be at least 18 years old.")
                continue
            break

        while True:
            chess_id = self.view.get_chess_id()
            if validate_chess_id(chess_id):
                break
            self.view.show_message("Invalid chess ID format. two letters and five digits required (e.g., AB12345).")

        player_data = {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "chess_id": chess_id.upper()
        }
        player = Player(**player_data)
        self.save_data(player.model_dump(exclude='point'), 'players')
        self.view.show_message("Player added successfully!")

    def list_players(self):
        """
        List all players in the database.
        This method loads all players from the database and displays them through the view.
        Returns:
            None
        Side Effects:
            - Displays a list of all players to the console
        """
        # call load_players from datamanager
        players = self.load_data('players')
        self.view.display_players(players)
