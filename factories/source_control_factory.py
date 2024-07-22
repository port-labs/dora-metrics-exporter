
from source_controls.github.service import GitHubSourceControl
from source_controls.gitlab.gitlab import GitLabSourceControl
from source_controls.azure_devops.azure import AzureDevOpsSourceControl
from interfaces.source_control import SourceControlInterface

class SourceControlFactory:
    
    @staticmethod
    def get_source_control(system: str) -> SourceControlInterface:
        if system == 'github':
            return GitHubSourceControl()
        elif system == 'gitlab':
            return GitLabSourceControl()
        elif system == 'azure_devops':
            return AzureDevOpsSourceControl()
        else:
            raise ValueError(f"Unknown source control system: {system}")
            