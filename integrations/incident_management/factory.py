
from port_dora.core.interfaces.incident_management import IncidentManagementInterface
from pagerduty.incident import PagerDutyIncident
from opsgenie.incident import OpsGenieIncident
from datadog.incident import DatadogIncident


class IncidentManagementFactory:
    _incident_management_map = {
        'pagerduty': PagerDutyIncident,
        'opsgenie': OpsGenieIncident,
        'datadog': DatadogIncident
    }

    @staticmethod
    def get_incident_management(integration: str) -> IncidentManagementInterface:
        try:
            return IncidentManagementFactory._incident_management_map[integration]()
        except KeyError:
            raise ValueError(f"Unknown incident management system: {integration}")