from pydantic import BaseModel


class Player(BaseModel):
    last_name: str
    first_name: str
    birth_date: str
    chess_id: str
    point: float = 0.0

    def to_dict(self):
        """
        Convert player instance to a dictionary.
        Returns:
            dict: A dictionary containing the player's information with the following keys:
                - last_name (str): The player's last name
                - first_name (str): The player's first name
                - birth_date (str): The player's birth date
                - chess_id (str): The player's chess ID
        """

        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id
        }

    def __hash__(self):
        """
        Calculate the hash value of the player instance.
        The hash value is based on the chess_id attribute, making the player
        object usable as a dictionary key or in sets.
        Returns:
            int: Hash value derived from the player's chess_id.
        """

        return hash(self.chess_id)

    def __eq__(self, other):
        """
        Check if two player instances are equal.
        Two player instances are considered equal if they have the same chess_id.
        Args:
            other (Player): The other player instance to compare
        Returns:
            bool: True if the two player instances are equal, False otherwise.
        """

        if not isinstance(other, Player):
            return False
        return self.chess_id == other.chess_id
