from abc import ABC, abstractmethod
from typing import List, Dict
from models import MergeRequest, Commit, Service


class SourceControlInterface(ABC):
    
    @abstractmethod
    async def get_commits(self,service: Service) -> List[Commit]:
        pass

    @abstractmethod
    async def get_merge_requests(service:Service) -> List[MergeRequest]:
        pass

    @abstractmethod
    async def get_services(self) -> List[Dict]:
        pass

    
class IncidentManagementInterface(ABC):
    
    @abstractmethod
    def get_incident_data(self) -> List[Dict]:
        pass


class CICDInterface(ABC):
    
    @abstractmethod
    def get_pipeline_data(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_deployment_data(self) -> List[Dict]:
        pass