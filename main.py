
from factories.source_control_factory import SourceControlFactory
from metrics.dora_metrics_calculator import DoraMetricsCalculator
from loguru import logger


def main(system: str):
    source_control = SourceControlFactory.get_source_control(system)
    dora_calculator = DoraMetricsCalculator(source_control)
    
    deployment_frequency = dora_calculator.compute_deployment_frequency()
    lead_time_for_changes = dora_calculator.compute_lead_time_for_changes()
    change_failure_rate = dora_calculator.compute_change_failure_rate()
    mttr = dora_calculator.compute_mttr()
    
    logger.info(f"Deployment Frequency: {deployment_frequency}")
    logger.info(f"Lead Time for Changes: {lead_time_for_changes}")
    logger.info(f"Change Failure Rate: {change_failure_rate}")
    logger.info(f"Mean Time to Recovery: {mttr}")

if __name__ == "__main__":
    main('github')  # Replace 'github' with 'gitlab' or 'azure_devops' as needed