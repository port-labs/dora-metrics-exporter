from abc import ABC, abstractmethod
from typing import List, Dict

class IncidentManagementInterface(ABC):
    
    @abstractmethod
    def get_incident_data(self) -> List[Dict]:
        pass
