from views.interface_view import InterfaceView


class TournamentView(InterfaceView):

    def __init__(self):
        super().__init__()
        self.players = []
        print("Welcome to the tournament manager!")

    def set_players_list(self, players):
        """
        Sets a list of players for the tournament.
        Args:
            players (list): A list of Player objects to be associated with the tournament
        Returns:
            None
        """

        self.players = players

    def get_tournament_details(self):
        """Gets tournament details from user input.
        This method prompts the user to enter various tournament details including name,
        location, start date, end date, list of players, and description.
        Returns:
            dict: A dictionary containing the tournament details with the following keys:
                - name (str): Name of the tournament
                - location (str): Location where tournament takes place
                - startDate (str): Start date in YYYY-MM-DD format
                - endDate (str): End date in YYYY-MM-DD format
                - playerList (list): List of selected players
                - description (str): Tournament description
        """

        print("Create tournament")
        tournament_name = input("Name: ")
        tournament_location = input("Location : ")
        startDate = input("Start date (YYYY-MM-DD) : ")
        endDate = input("End date (YYYY-MM-DD) : ")
        playerList = self.select_players()
        description = input("Description : ")
        # créer l'objet ici et le retourner
        return {"name": tournament_name, "location": tournament_location,
                "startDate": startDate, "endDate": endDate, "playerList": playerList, "description": description}

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
