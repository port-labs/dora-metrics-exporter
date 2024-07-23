from pydantic import BaseModel
from typing import List
from datetime import datetime


class Service(BaseModel):
    id: str
    name: str
    created_at: str


class Commit(BaseModel):
    id: str
    message: str
    author: str
    timestamp: str


class Branch(BaseModel):
    name: str


class MergeRequestReview(BaseModel):
    id: str
    reviewer: str
    timestamp: str


class MergeRequest(BaseModel):
    id: str
    status: str
    created_at: str | None
    closed_at: str 
    branch: Branch
    commits: List[Commit]
    reviews: List[MergeRequestReview]
    class Config:
        extra = "allow"
    

class SourceControl(BaseModel):
    service: Service
    branch: str
    merge_requests: List[MergeRequest]
    
    class Config:
        extra = "allow"


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
