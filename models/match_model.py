from typing import List, Tuple
from pydantic import BaseModel
from models.player_model import Player

MATCH_NULL_SCORE = 0.5
MATCH_WIN_SCORE = 1.0
MATCH_LOOSE_SCORE = 0.0
SCORE_MAPPING = {
    0: (MATCH_NULL_SCORE, MATCH_NULL_SCORE),
    1: (MATCH_WIN_SCORE, MATCH_LOOSE_SCORE),
    2: (MATCH_LOOSE_SCORE, MATCH_WIN_SCORE)
}


class Match(BaseModel):
    match: Tuple[List[Player | float], List[Player | float]]
