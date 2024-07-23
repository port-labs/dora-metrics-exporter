from .github.service import GitHubSourceControl
from .gitlab.service import GitLabSourceControl
from .azure_devops.service import AzureDevOpsSourceControl
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source_control.interface import SourceControlInterface

class SourceControlFactory:
    _source_control_map = {
        'github': GitHubSourceControl,
        'gitlab': GitLabSourceControl,
        'azure_devops': AzureDevOpsSourceControl
    }

    @staticmethod
    def get_source_control(integration: str) -> SourceControlInterface:
        try:
            return SourceControlFactory._source_control_map[integration]()
        except KeyError:
            raise ValueError(f"Unknown source control system: {integration}")