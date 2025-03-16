from typing import Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3