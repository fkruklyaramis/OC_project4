from pydantic import BaseModel
from datetime import datetime
from typing import List


class Round(BaseModel):
    """A class representing a round in a tournament.

    This class inherits from BaseModel and manages round-related information including
    round number, name, list of matches, and start/end dates.

    Attributes:
        number (int): The round number
        name (str): The name of the round (default: None)
        matchList (List): List containing the matches in this round (default: empty list)
        startDate (str): The start date and time of the round in format 'YYYY-MM-DD HH:MM:SS'
                         (default: current date/time)
        endDate (str): The end date and time of the round in format 'YYYY-MM-DD HH:MM:SS'
                       (default: None)
    """
    number: int
    name: str = None
    matchList: List = []
    startDate: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    endDate: str = None
