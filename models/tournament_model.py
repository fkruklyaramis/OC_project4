from typing import Optional
from pydantic import BaseModel, Field
from typing import List
from models.player_model import Player


class Tournament(BaseModel):
    name: str
    location: str
    startDate: str
    endDate: str
    roundNumber: int = Field(default=4)
    roundId: Optional[int] = Field(default=None)
    roundList: List[dict] = []
    playerList: List[Player]
    description: str

    def to_dict(self):
        """
        Convert tournament instance to a dictionary.
        Returns:
            dict: A dictionary containing the tournament's information with the following keys:
                - name (str): The tournament's name
                - location (str): The tournament's location
                - startDate (str): The tournament's start date
                - endDate (str): The tournament's end date
                - roundNumber (int): The number of rounds in the tournament
                - roundId (int): The current round ID
                - roundList (list): A list of round details
                - playerList (list): A list of player details
                - description (str): The tournament's description
        """

        return {
            "name": self.name,
            "location": self.location,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "roundNumber": self.roundNumber,
            "roundId": self.roundId,
            "roundList": self.roundList,
            "playerList": self.playerList,
            "description": self.description
        }
