import asyncio
from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union, Callable, AsyncIterator, TypeVar, Any, Dict
from github import Github, GithubException
from github.PaginatedList import PaginatedList
from github.Branch import Branch
from github import (
    PullRequest as GithubPullRequest,
    Workflow as GithubWorkflow,
    WorkflowRun as GithubWorkflowRun,
    Team as GithubTeam
)
from loguru import logger


T = TypeVar("T", bound=Union[GithubPullRequest, GithubTeam])

DEFAULT_PAGINATION_PAGE_SIZE = 100


class AsyncFetcher:
    @staticmethod
    async def fetch_single(
        fetch_func: Callable[..., T],
        *args,
    ) -> T:
        with ThreadPoolExecutor() as executor:
            return await get_event_loop().run_in_executor(executor, fetch_func, *args)

    @staticmethod
    async def fetch_batch(
        fetch_func: Callable[..., PaginatedList],
        validation_func: Callable[[Any], bool] = None,
        page_size: int = DEFAULT_PAGINATION_PAGE_SIZE,
        **kwargs,
    ) -> AsyncIterator[List[T]]:
        def fetch_page(page_idx: int) -> List[T]:
            logger.info(f"Fetching page {page_idx}. Page size: {page_size}")
            paginated_list = fetch_func(**kwargs)
            return paginated_list.get_page(page_idx)

        page = 0
        while True:
            batch = None
            try:
                batch = await asyncio.get_running_loop().run_in_executor(
                    None, fetch_page, page
                )
                print("Batch Total Count",batch.totalCount)
            except GithubException as err:
                logger.warning(f"Failed to access resource, error={err}")
                break
            if not batch:
                logger.info(f"No more items to fetch after page {page}")
                break
            logger.info(f"Queried {len(batch)} items before filtering")

            yield list(validation_func(batch)) if validation_func else batch

            page += 1