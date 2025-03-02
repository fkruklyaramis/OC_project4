from views.interface_view import InterfaceView


class PlayerView(InterfaceView):

    def get_player_details(self):
        """
        Gets player details from user input.
        This method prompts the user to enter player information including:
        - Last name
        - First name
        - Birth date (in YYYY-MM-DD format)
        - Chess ID
        Returns:
            dict: A dictionary containing the player details with keys:
                - last_name (str)
                - first_name (str)
                - birth_date (str)
                - chess_id (str)
        """

        print("Add a player :")
        last_name = input("Last name : ")
        first_name = input("First name : ")
        birth_date = input("Birth date (YYYY-MM-DD) : ")
        chess_id = input("Chess id : ")
        return {"last_name": last_name, "first_name": first_name, "birth_date": birth_date, "chess_id": chess_id}

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
        for player in players:
            print(f"{player['chess_id']} - {player['last_name']} {player['first_name']} "
                  f"{player['birth_date']}")

    def show_message(self, message: str):
        """Display a message to the user"""
        print(f"\n{message}")
