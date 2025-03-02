import json


class DataManager:
    def __init__(self):
        self.tournaments_file = "./data/tournaments.json"
        self.players_file = "./data/players.json"

    def load_tournaments(self):
        """
        Load tournaments from a JSON file.
        This method reads tournament data from a specified JSON file.
        If the file is not found, it returns an empty list.
        Returns:
            list: A list of tournament dictionaries. Returns an empty list if file not found.
        """

        try:
            with open(self.tournaments_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def load_players(self):
        """
        Load players data from a JSON file.
        This method attempts to read player data from the specified JSON file.
        If the file is not found, it returns an empty list.
        Returns:
            list: A list of player dictionaries if file exists,
                  or an empty list if file is not found
        """

        try:
            with open(self.players_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_player(self, player_data: dict):
        """
        Save a player's data to the JSON file containing all players.

        Args:
            player_data (dict): Dictionary containing player's information with following keys:
                - last_name (str): Player's last name
                - first_name (str): Player's first name
                - birth_date (str): Player's birth date
                - chess_id (str): Player's unique chess identifier
                - ranking (int): Player's chess ranking

        Returns:
            None

        Note:
            The player data is appended to the existing list of players in the JSON file.
        """

        players = self.load_players()
        players.append(player_data)
        with open(self.players_file, "w") as file:
            json.dump(players, file, indent=4)

    def save_tournament(self, tournament_data: dict):
        """
        Save a tournament's data to the tournaments file.

        This method appends a new tournament's data to the existing list of tournaments
        and saves it to the JSON file.

        Args:
            tournament_data (dict): A dictionary containing the tournament information
                                   to be saved

        Returns:
            None

        Example:
            tournament_data = {
                "name": "Chess Championship 2023",
                "date": "2023-01-01",
                "players": [...],
                "rounds": [...]
            }
            data_manager.save_tournament(tournament_data)
        """

        tournaments = self.load_tournaments()
        tournaments.append(tournament_data)
        with open(self.tournaments_file, "w") as file:
            json.dump(tournaments, file, indent=4)
