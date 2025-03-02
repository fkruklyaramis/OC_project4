from models.player_model import Player
from views.player_view import PlayerView
from models.data_manager import DataManager


class PlayerController(DataManager):

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
        Add a new player to the database.
        This method collects player details through the view, creates a new Player instance,
        and saves it to the database.
        Returns:
            None
        Side Effects:
            - Creates a new player entry in the database
            - Prints success message to console
        """

        data = self.view.get_player_details()
        player = Player(**data)
        # call save_player from datamanager
        self.save_player(player.to_dict())
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
        players = self.load_players()
        self.view.display_players(players)
