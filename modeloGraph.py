from typing import List, Optional
from pydantic import BaseModel
class modeloRota(BaseModel):
    source: str
    target: str
    distance: int

class payload(BaseModel):
    id: Optional[int]
    data:list[modeloRota]

