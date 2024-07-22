from __future__ import annotations
import asyncio
from source_control.interface import SourceControlInterface
from typing import TYPE_CHECKING, List, AsyncIterator, Callable
from loguru import logger
from client import github_client
from models import Commit, SourceControl, Service, MergeRequest, Branch, MergeRequestReview

if TYPE_CHECKING:
    from github.Repository import Repository
    from github.PullRequest import PullRequest

class GitHubSourceControl(SourceControlInterface):

    
    async def _get_commits(self,pull_request:PullRequest)-> List[Commit]:
        return [Commit(id=commit.id,
                      timestamp=commit.timestamp)
                    async for commits in github_client.get_pull_request_commits(pull_request)
                    for commit in commits]


    async def _get_reviews(self,pull_request:PullRequest) -> List[MergeRequestReview]:
        return [MergeRequestReview(id=review.id,
                                 reviewer=review.reviewer,
                                 timestamp=review.timestamp)
                async for reviews in github_client.get_pull_request_reviews(pull_request)
                for review in reviews]
    

    async def fetch_all_commits(self, service_id: str) -> AsyncIterator[List[Commit]]:
        async for merge_request in github_client.get_pull_requests(service_id):
            yield self._get_commits(merge_request)


    async def fetch_all_reviews(self, service_id: str)-> AsyncIterator[List[MergeRequestReview]]:
        async for merge_request in github_client.get_pull_requests(service_id):
            yield self._get_reviews(merge_request)
            
        
    async def fetch_merge_requests(self, service_id: str) -> AsyncIterator[MergeRequest]:
        async for merge_request_data in github_client.get_pull_requests(service_id):
            
            task = [ MergeRequest(
                **merge_request_data,
                commits=lambda: self._get_commits(merge_request_data),
                reviews=lambda: self._get_reviews(merge_request_data)
            ) for merge_request in merge_request_data]
            
            merge_requests = await asyncio.gather(*task)
            yield merge_requests


    async def get_services(self) -> AsyncIterator[List[Service]]:
        
        async def cast_repos_to_service(repos:List[Repository]) -> Service:

            task = [Service(
                    id=repo.id,
                    name=repo.name,
                    url=repo.html_url
                ) for repo in repos
            ]
            services = List[Service] = await asyncio.gather(*task)
            return services

        tasks = [cast_repos_to_service(repos) async for repos in github_client.get_repositories()]
        async for task in asyncio.as_completed(tasks):
            yield task


    async def __call__(self, branch: str) -> AsyncIterator[SourceControl]:
        async for services in self.get_services():
            for service in services:
                merge_requests = lambda: self.fetch_merge_requests(service.id)
                yield SourceControl(
                    service=service,
                    branch=Branch(branch),
                    merge_requests=merge_requests
                )
