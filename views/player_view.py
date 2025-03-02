from views.interface_view import InterfaceView


class PlayerView(InterfaceView):
    """A class for handling player-related views and user interactions.

    This class extends InterfaceView and provides methods for getting player information
    from user input and displaying player data.

    Methods:
        get_last_name(): Get player's last name from user input
        get_first_name(): Get player's first name from user input
        get_birth_date(): Get player's birth date from user input
        get_chess_id(): Get player's chess ID from user input
        display_players(players): Display a list of players with their details
        show_message(message): Display a message to the user

    Attributes:
        Inherits from InterfaceView
    """

    def get_last_name(self):
        """Get player's last name from user input."""
        return input("Last name : ")

    def get_first_name(self):
        """Get player's first name from user input."""
        return input("First name : ")

    def get_birth_date(self):
        """Get player's birth date from user input."""
        return input("Birth date (YYYY-MM-DD) : ")

    def get_chess_id(self):
        """Get player's chess ID from user input."""
        return input("Chess id (format: AB12345) : ")

    def display_players(self, players):
        """
        Displays a list of players.
        This method prints a list of players with their details.
        Args:
            players (list): A list of dictionaries containing player details
        Returns:
            None
        """

        print("\nPlayer list :")
        if not players:
            print("No players found.")
            return
        for player in players:
            print(f"{player['chess_id']} - {player['last_name']} {player['first_name']} "
                  f"{player['birth_date']}")

    def show_message(self, message: str):
        """Display a message to the user"""
        print(f"\n{message}")
