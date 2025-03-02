from pydantic import BaseModel


class Player(BaseModel):
    """Represents a chess player.

    This class provides a data model for storing and managing chess player information.
    Inherits from BaseModel and provides functionality for player data management.

    Attributes:
        last_name (str): The player's last name
        first_name (str): The player's first name
        birth_date (str): The player's date of birth
        chess_id (str): Unique identifier for the player in the chess system
        point (float): The player's current points/score, defaults to 0.0
    """
    last_name: str
    first_name: str
    birth_date: str
    chess_id: str
    point: float = 0.0

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
