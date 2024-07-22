import typing
from typing import TYPE_CHECKING, List, Dict,Any, AsyncIterator
from github import Github, Workflow, WorkflowRun, Deployment
from datetime import datetime
from loguru import logger
from asyncFetcher import AsyncFetcher
import asyncio
from utils import cache

if TYPE_CHECKING:
    from github.Repository import Repository
    from github.Workflow import Workflow
    from github.Workflow import WorkflowRun
    from github.Deployment import Deployment


class CACHE_KEYS:
    WORKFLOWS_CACHE_KEY:str = "__WORKFLOWS_CACHE_KEY"
    REPOSITORY_CACHE_KEY:str = "__REPOSITORIES_CACHE_KEY"

class GitHubActionsClient:
    def __init__(self, owner: str, token: str):
        self.owner:str = owner
        self.token:str = token
        self.reference_datetime:datetime = self.set_reference_datetime
        self.github = Github(login_or_token=token)

    @property
    def set_reference_datetime(self,number_of_days:int)->datetime:
        reference_datetime:datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=number_of_days)
        return reference_datetime
    
    def _is_within_timeframe(self, created_at):
        end_date = datetime.datetime.now(datetime.timezone.utc)
        start_date = end_date - datetime.timedelta(days=self.number_of_days)
        return start_date <= created_at <= end_date

    def _filter_workflows_runs(self, runs: List[Workflow.WorkflowRun]) -> List[Work]:
        return list(filter(lambda run: run.head_branch == self.branch and self._is_within_timeframe(run.created_at.replace(tzinfo=None)), runs))
        
    def _filter_deployments(self,deployments:List[Deployment.Deployment])->List[Deployment.Deployment]:
        return list(filter(lambda dep: dep.created_at.replace(tzinfo = None) > self.reference_datetime,deployments))
    
    def _filter_deployment(self,deployment:Deployment.Deployment):
        return self._is_within_timeframe(deployment.created_at)
       
    async def _get_repository(self,id:str) -> Repository:
        if cached_repositories := await cache.get(CACHE_KEYS.REPOSITORY_CACHE_KEY):
            if repository := cached_repositories.get(id):
                return repository      
        repository = await AsyncFetcher.fetch_single(fetch_func=self.github.org.get_repos)
        repository: Repository = typing.cast(Repository, repository)
        return repository
    
    async def get_deployments(self,repository_id:str)-> AsyncIterator[List[Deployment]]:
        repository = await self._get_repository(repository_id)
        async for deployments in AsyncFetcher.fetch_batch(repository.get_deployments):
            deployments:List[Deployment] = typing.cast(List[Deployment], deployments)
            yield deployments

    async def get_workflow_runs(self, workflow: Workflow)-> AsyncIterator[List[WorkflowRun]]:
        async for runs in AsyncFetcher.fetch_batch(workflow.get_runs):
            runs: List[WorkflowRun] = typing.cast(List[WorkflowRun], runs)
            yield runs
            

    async def get_workflows(self,repository_id) ->  AsyncIterator[List[Workflow]]:

        if cached_workflows := self.cache.get(CACHE_KEYS.WORKFLOWS_CACHE_KEY):
            yield list(cached_workflows.values())
            return

        repository:Repository = await self._get_repository(repository_id)
        async for workflows in AsyncFetcher.fetch_batch(repository.get_workflows):
            workflows: Workflow = typing.cast(List[Workflow], workflows)
            cache.upsert(CACHE_KEYS.WORKFLOWS_CACHE_KEY,{workflow.id:workflow for workflow in workflows})
            yield workflows


    async def get_workflow_runs(self, repository_id:str) -> AsyncIterator[List[WorkflowRun]]:
        repository = await self._get_repository(repository_id)
        async for runs in AsyncFetcher.fetch_batch(repository.get_workflow_runs):
            runs: List[WorkflowRun] = typing.cast(List[WorkflowRun], runs)
            yield runs


github_actions_client = GitHubActionsClient()