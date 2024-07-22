from integrations.source_control.github_source_control import GitHubSourceControl
from integrations.source_control.gitlab_source_control import GitLabSourceControl
from integrations.source_control.azure_devops_source_control import AzureDevOpsSourceControl

from integrations.cicd.github_actions import GitHubActions
from integrations.cicd.gitlab_ci import GitLabCI
from integrations.cicd.azure_pipelines import AzurePipelines

from integrations.incident_management.pagerduty import PagerDuty
from integrations.incident_management.opsgenie import OpsGenie
from integrations.incident_management.datadog import Datadog

from interfaces.source_control import SourceControlInterface
from interfaces.cicd import CICDInterface
from interfaces.incident_management import IncidentManagementInterface

class SourceControlFactory:
    _source_control_map = {
        'github': GitHubSourceControl,
        'gitlab': GitLabSourceControl,
        'azure_devops': AzureDevOpsSourceControl
    }

    @staticmethod
    def get_source_control(system: str) -> SourceControlInterface:
        try:
            return SourceControlFactory._source_control_map[system]()
        except KeyError:
            raise ValueError(f"Unknown source control system: {system}")

class CICDFactory:
    _cicd_map = {
        'github_actions': GitHubActions,
        'gitlab_ci': GitLabCI,
        'azure_pipelines': AzurePipelines
    }

    @staticmethod
    def get_cicd(system: str) -> CICDInterface:
        try:
            return CICDFactory._cicd_map[system]()
        except KeyError:
            raise ValueError(f"Unknown CI/CD system: {system}")

class IncidentManagementFactory:
    _incident_management_map = {
        'pagerduty': PagerDuty,
        'opsgenie': OpsGenie,
        'datadog': Datadog
    }

    @staticmethod
    def get_incident_management(system: str) -> IncidentManagementInterface:
        try:
            return IncidentManagementFactory._incident_management_map[system]()
        except KeyError:
            raise ValueError(f"Unknown incident management system: {system}")

# Unified Integration Factory
class IntegrationFactory:
    @staticmethod
    def get_source_control(system: str) -> SourceControlInterface:
        return SourceControlFactory.get_source_control(system)

    @staticmethod
    def get_cicd(system: str) -> CICDInterface:
        return CICDFactory.get_cicd(system)

    @staticmethod
    def get_incident_management(system: str) -> IncidentManagementInterface:
        return IncidentManagementFactory.get_incident_management(system)

# Usage
if __name__ == "__main__":
    source_control = IntegrationFactory.get_source_control('github')
    cicd = IntegrationFactory.get_cicd('gitlab_ci')
    incident_management = IntegrationFactory.get_incident_management('pagerduty')

    print(source_control)  # Output: Instance of GitHubSourceControl
    print(cicd)  # Output: Instance of GitLabCI
    print(incident_management)  # Output: Instance of PagerDuty
