class CICDFactory:
    _cicd_map = {
        'github_actions': GitHubActions,
        'gitlab_ci': GitLabCI,
        'azure_pipelines': AzurePipelines
    }

    @staticmethod
    def get_cicd(integration: str) -> CICDInterface:
        try:
            return CICDFactory._cicd_map[integration]()
        except KeyError:
            raise ValueError(f"Unknown CI/CD integration: {integration}")