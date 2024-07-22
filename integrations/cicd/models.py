from pydantic import BaseModel
from datetime import datetime
from typing import List


class Deployment(BaseModel):
    id: int
    name: str
    environment: str
    timestamp: datetime
    status: str


class Pipeline(BaseModel):
    id: int
    name: str
    deployments: List[Deployment]
    frequency: int