from interfaces.cicd import CICDInterface
from typing import List, Dict, AsyncIterator
from client import github_actions_client
from models import Pipeline, Deployment
import asyncio

class GitHubActions(CICDInterface):
    
    async def _get_pipeline_deployments(pipeline) -> List[Deployment]:
        return [Deployment(id = run.id,
                           name= run,
                           environment = run.environment,
                           timestamp = run.created_at)
                           async for runs in github_actions_client.get_workflow_runs(pipeline)
                           for run in runs]


    async def get_pipeline_data(self, service) -> AsyncIterator[List[Pipeline]]:
        """
        Implements GitHub Actions-specific logic to fetch pipeline data
        """
        async for workflows in github_actions_client.get_workflows():
            tasks: List[Pipeline] = [Pipeline(
                id = workflow.id,
                name= workflow.name,
                deployments=lambda: self._get_pipeline_deployments(workflow)
            ) for workflow in workflows]
            
            pipelines = await asyncio.gather(*tasks)
            yield pipelines


    async def get_deployment_data(self) -> AsyncIterator[List[Deployment]]:
        """
        Implements GitHub specific logic to fetch deployment data
        """
        async for deployments in github_actions_client.get_deployments():
            tasks: List[Deployment] = [ Deployment(
                id = deployment.id,
                name= deployment.name,
                environment = deployment.environment,
                timestamp = deployment.created_at,
                status = str
            ) for deployment in deployments]
            
            pipelines = await asyncio.gather(*tasks)
            yield pipelines