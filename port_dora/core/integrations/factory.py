from port_docainterfaces.source_control import SourceControlInterface
from port_dora.core.integrations.interfaces import CICDInterface, IncidentManagementInterface, SourceControlInterface
from interfaces.cicd import CICDInterface
from interfaces.incident_management import IncidentManagementInterface

from integrations.source_control.factory import SourceControlFactory
from integrations.cicd.factory import CICDFactory
from integrations.incident_management.factory import IncidentManagementFactory


# Unified Integration Factory
class IntegrationFactory:
    @staticmethod
    def get_source_control(integration: str) -> SourceControlInterface:
        return SourceControlFactory.get_source_control(integration)

    @staticmethod
    def get_cicd(integration: str) -> CICDInterface:
        return CICDFactory.get_cicd(integration)

    @staticmethod
    def get_incident_management(integration: str) -> IncidentManagementInterface:
        return IncidentManagementFactory.get_incident_management(integration)
