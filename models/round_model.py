from pydantic import BaseModel
from datetime import datetime
from typing import List


class Round(BaseModel):
    number: int
    name: str = None
    matchList: List = []
    startDate: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    endDate: str = None

    def to_dict(self):
        """
        Convert round instance to a dictionary.
        Returns:
            dict: A dictionary containing the round's information with the following keys:
                - number (int): The round number
                - name (str): The round name
                - matchList (list): A list of match results
                - startDate (str): The round start date
                - endDate (str): The round end date
        """
        return {
            "number": self.number,
            "name": self.name,
            "matchList": self.matchList,
            "startDate": self.startDate,
            "endDate": self.endDate
        }
