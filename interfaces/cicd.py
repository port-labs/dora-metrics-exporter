from abc import ABC, abstractmethod
from typing import List, Dict

class CICDInterface(ABC):
    
    @abstractmethod
    def get_pipeline_data(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_deployment_data(self) -> List[Dict]:
        pass
