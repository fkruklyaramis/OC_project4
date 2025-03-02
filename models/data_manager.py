import json
import os


class DataManager:
    """"
    A class to manage data persistence for the chess tournament application.
    This class handles all data storage and retrieval operations for tournaments
    and players, using JSON files as the storage medium.
    Attributes:
        data_directory (str): Path to the directory where data files are stored
        tournaments_file (str): Path to the JSON file storing tournament data
        players_file (str): Path to the JSON file storing player data
    """
    def __init__(self):
        self.data_directory = "./data"
        self.tournaments_file = os.path.join(self.data_directory, "tournaments.json")
        self.players_file = os.path.join(self.data_directory, "players.json")
        self._initialize_data_files()

    def _initialize_data_files(self):
        """
        Initialize data directory and JSON files if they don't exist.
        Creates the data directory and empty JSON files for tournaments and players.
        """
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        # Create empty JSON files if they don't exist
        for file_path in [self.tournaments_file, self.players_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    json.dump([], file)

    def load_data(self, data_type: str) -> list:
        """
        Load data from a JSON file based on the specified type.

        Args:
            data_type (str): Type of data to load ('tournaments' or 'players')

        Returns:
            list: A list of dictionaries containing the requested data

        Raises:
            ValueError: If data_type is not 'tournaments' or 'players'
        """
        if data_type not in ['tournaments', 'players']:
            raise ValueError("data_type must be 'tournaments' or 'players'")

        file_path = self.tournaments_file if data_type == 'tournaments' else self.players_file
        try:
            with open(file_path, "r") as file:
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

    def save_data(self, data: dict, data_type: str) -> None:
        """
        Save data to the appropriate JSON file based on the specified type.

        Args:
            data (dict): Dictionary containing the data to save
            data_type (str): Type of data to save ('tournaments' or 'players')

        Raises:
            ValueError: If data_type is not 'tournaments' or 'players'
        """
        if data_type not in ['tournaments', 'players']:
            raise ValueError("data_type must be 'tournaments' or 'players'")

        file_path = self.tournaments_file if data_type == 'tournaments' else self.players_file
        current_data = self.load_data(data_type)
        current_data.append(data)

        with open(file_path, "w") as file:
            json.dump(current_data, file, indent=4)
