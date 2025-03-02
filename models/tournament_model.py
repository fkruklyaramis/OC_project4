from typing import Optional
from pydantic import BaseModel, Field
from typing import List
from models.player_model import Player


class Tournament(BaseModel):
    """Tournament class represents a chess tournament with its essential details.

    This class inherits from BaseModel and contains information about a chess tournament,
    including its name, location, dates, rounds, players and description.

    Attributes:
        name (str): The name of the tournament
        location (str): Where the tournament takes place
        startDate (str): The start date of the tournament
        endDate (str): The end date of the tournament
        roundNumber (int): Number of rounds in the tournament, defaults to 4
        roundId (Optional[int]): Current round ID, defaults to None
        roundList (List[dict]): List containing information about tournament rounds
        playerList (List[Player]): List of players participating in the tournament
        description (str): Description or additional notes about the tournament
    """

    name: str
    location: str
    startDate: str
    endDate: str
    roundNumber: int = Field(default=4)
    roundId: Optional[int] = Field(default=None)
    roundList: List[dict] = []
    playerList: List[Player]
    description: str
