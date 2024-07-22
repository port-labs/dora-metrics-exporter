from abc import ABC, abstractmethod
from typing import List, Dict
from models import MergeRequest, Commit, Service


class SourceControlInterface(ABC):
    
    @abstractmethod
    def get_commits(self,service: Service) -> List[Commit]:
        pass

    @abstractmethod
    def get_merge_requests(service:Service) -> List[MergeRequest]:
        pass

    @abstractmethod
    def get_services(self) -> List[Dict]:
        pass