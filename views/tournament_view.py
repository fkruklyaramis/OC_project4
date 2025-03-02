from views.interface_view import InterfaceView


class TournamentView(InterfaceView):
    """
    A view class for managing tournament-related user interactions.

    This class handles the display and input collection for tournament management,
    including player selection, tournament details input, and message display.

    Attributes:
        players (list): A list of player dictionaries containing player information.

    Methods:
        set_players_list(players): Sets the list of available players.
        get_name(): Gets tournament name from user input.
        get_location(): Gets tournament location from user input.
        get_start_date(): Gets tournament start date from user input.
        get_end_date(): Gets tournament end date from user input.
        get_description(): Gets tournament description from user input.
        show_message(message): Displays a message to the user.
        select_players(): Allows user to select players for the tournament.

    Inherits From:
        InterfaceView: Base class for view interfaces.
    """
    def __init__(self):
        super().__init__()
        self.players = []
        print("\nWelcome to the tournament manager!")

    def set_players_list(self, players):
        """
        Sets a list of players for the tournament.
        Args:
            players (list): A list of Player objects to be associated with the tournament
        Returns:
            None
        """

        self.players = players

    def get_name(self):
        """Get tournament name from user input."""
        return input("Name: ")

    def get_location(self):
        """Get tournament location from user input."""
        return input("Location: ")

    def get_start_date(self):
        """Get tournament start date from user input."""
        return input("Start date (YYYY-MM-DD): ")

    def get_end_date(self):
        """Get tournament end date from user input."""
        return input("End date (YYYY-MM-DD): ")

    def get_description(self):
        """Get tournament description from user input."""
        return input("Description: ")

    def show_message(self, message: str):
        """Display a message to the user"""
        print(f"\n{message}")

    def select_players(self) -> list:
        """
        Allows user to select players from a list of available players.
        This method displays all available players and prompts the user to select players
        by entering their chess IDs. It validates the selections and ensures an even number
        of unique players with a minimum of 2 players.

        Returns:
            list: A list of dictionaries containing the selected players' information.
              Returns empty list if no players are registered.
              Each player dictionary contains:
              - 'first_name': Player's first name
              - 'last_name': Player's last name
              - 'chess_id': Player's chess ID

        Validation:
            - Requires an even number of players
            - Minimum of 2 players required
            - All chess IDs must be valid

        Example:
            >>> view = TournamentView()
            >>> selected_players = view.select_players()
            Available players:
            - John Doe (ID: AB12345)
            - Jane Smith (ID: CD67890)
            Enter players' chess IDs (separated by comma): AB12345, CD67890
            Selected players:
            - John Doe (ID: AB12345)
            - Jane Smith (ID: CD67890)
        """

        if not self.players:
            print("No registered players.")
            return []

        print("\nAvailable players :")
        for player in self.players:
            print(f"- {player['first_name']} {player['last_name']} (ID: {player['chess_id']})")

        while True:
            selected_ids = input("\nEnter players' chess IDs (separated by comma): ").strip().split(',')
            selected_ids = list(dict.fromkeys([id.strip() for id in selected_ids if id.strip()]))

            # Check for even number of players
            if len(selected_ids) % 2 != 0:
                print("\nError: Please select an even number of unique players")
                continue

            player_list = []
            invalid_ids = False

            for chess_id in selected_ids:
                player = next((p for p in self.players if p['chess_id'] == chess_id), None)
                if player:
                    player_list.append(player)
                else:
                    print(f"Chess ID {chess_id} unknown")
                    invalid_ids = True
                    break

            if invalid_ids:
                continue

            # Ensure at least 2 players
            if len(player_list) >= 2:
                print("\nSelected players:")
                for player in player_list:
                    print(f"- {player['first_name']} {player['last_name']} (ID: {player['chess_id']})")
                return player_list
            else:
                print("\nError: Please select at least 2 players.")

    def display_single_winner(self, winner):
        """
        Display information for a single tournament winner.
        Args:
            winner: Player object representing the tournament winner
        """
        self.show_message(
            f"Tournament Winner: {winner.first_name} {winner.last_name} "
            f"with {winner.point} points!"
        )

    def display_tie(self, winners, points):
        """
        Display information when tournament ends in a tie.
        Args:
            winners (list): List of Player objects who tied for first
            points (float): The winning point total
        """
        self.show_message("Tournament ended in a tie!")
        print("Winners with", points, "points:")
        for player in winners:
            print(f"- {player.first_name} {player.last_name}")
