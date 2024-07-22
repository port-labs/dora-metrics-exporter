
from abc import ABC, abstractmethod
from typing import List, Dict

class SourceControlInterface(ABC):
    
    @abstractmethod
    def get_commit_data(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_deployment_data(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_services(self) -> List[Dict]:
        pass

    @abstractmethod
    def get_failure_data(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_recovery_data(self) -> List[Dict]:
        pass
            