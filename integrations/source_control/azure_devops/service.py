from __future__ import annotations
import asyncio
from interfaces.source_control import SourceControlInterface
from typing import TYPE_CHECKING, List, Dict, Any, AsyncIterator
from loguru import logger
from client import github_client
from models import Commit, SourceControl, Service

if TYPE_CHECKING:
    # import repository type from ado
    pass

class AzureDevopsSourceControl(SourceControlInterface):

    def get_commit_data(self) -> List[Dict]:
        # Implement GitHub-specific logic to fetch commit data
        pass
    
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
            