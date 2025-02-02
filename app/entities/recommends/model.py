from pydantic import BaseModel
from typing import List

class Recommendations(BaseModel):
    user_id: int
    recommended_films: List[int]
