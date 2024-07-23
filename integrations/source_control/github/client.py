# repository/github_repository.py
# from __future__ import annotations
import asyncio
from concurrent.futures import ThreadPoolExecutor
import typing
from typing import cast, TYPE_CHECKING, List, Dict, Any, Literal, AsyncGenerator, AsyncIterator
from github import Github, GithubObject, GithubException, Repository, PullRequest, NamedUser, Team, Membership, Issue, PullRequestReview, Commit
import datetime
from asyncFetcher import AsyncFetcher
from port_dora.utils.cache import cache
from loguru import logger


class CACHE_KEYS:
    PULL_REQUESTS_CACHE_KEY = "__PULL_REQUESTS_CACHE_KEY"
    TEAM_MEMBERS_CACHE_KEY = "__TEAM_MEMBERS_CACHE_KEY"
    TEAMS_CACHE_KEY:str = "__TEAM_CACHE_KEY"
    REPOSITORY_CACHE_KEY:str = "__REPOSITORIES_CACHE_KEY"

MAX_CONCURRENT_TASKS = 30


class GitHubClient:
    def __init__(self, owner: str, token: str):
        self.owner:str = owner
        self.token:str = token
        self.reference_datetime:datetime = self.set_reference_datetime
        self.github = Github(login_or_token=token)
        self.cache:Dict[str,Any] = {}


    @property
    def set_reference_datetime(self,number_of_days:int)->datetime:
        reference_datetime:datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=number_of_days)
        return reference_datetime
    
    def _is_within_timeframe(self, obj:GithubObject.GithubObject) -> bool:
        created_at = obj['created_at']
        end_date = datetime.datetime.now(datetime.timezone.utc)
        start_date = end_date - datetime.timedelta(days=self.number_of_days)
        return start_date <= created_at <= end_date

    def _filter_pull_requests(self, prs: List[PullRequest.PullRequest]) -> List[PullRequest.PullRequest]:
        return list(filter(lambda pr: pr.merged_at.isoformat() and pr.merge_commit_sha and self._is_within_timeframe(pr.merged_at.replace(tzinfo = None)), prs))


    async def get_pull_request_commits(self, pull_request: PullRequest.PullRequest) -> AsyncIterator[Commit.Commit]:
        async for commits in self.AsyncFetcher.fetch_batch(pull_request.get_commits):
            yield commits
        

    async def get_pull_request_reviews(self, pr: PullRequest.PullRequest) -> AsyncIterator[PullRequestReview.PullRequestReview]:
        async for reviews in AsyncFetcher.fetch_batch(pr.get_reviews,validation_func=self._is_within_timeframe):
            yield reviews


    async def enrich_pull_request_with_commits_and_reviews(self,pull_request: PullRequest.PullRequest) -> PullRequest:
        commits_task = asyncio.create_task(self.get_commits_for_pr(pull_request))
        reviews_task = asyncio.create_task(self.get_reviews_for_pr(pull_request))

        commits, reviews = await asyncio.gather(commits_task, reviews_task)
        pull_request.commits = commits
        pull_request.reviews = reviews
        return pull_request

    async def get_repositories(self) -> AsyncIterator[List[Repository.Repository]]:
        if not (cached_repositories := cache.get(CACHE_KEYS.REPOSITORY_CACHE_KEY)):
            async for repos_batch in AsyncFetcher.fetch_batch(fetch_func=self.github.org.get_repos):
                batch_repositories: List[Repository.Repository] = typing.cast(List[Repository.Repository], repos_batch)
                cache.upsert(CACHE_KEYS.REPOSITORY_CACHE_KEY, {repository.id: repository for repository in batch_repositories})
                yield batch_repositories
            cache.set(CACHE_KEYS.REPOSITORY_CACHE_KEY, cached_repositories)
            return
        return list(cached_repositories.values())


    async def get_pull_requests(self, repo, state: Literal['closed', 'open', 'all'] = 'closed', base:str | None = 'main') -> AsyncGenerator[PullRequest.PullRequest, None]:
        if not (pull_request_cache:= self._cache_get(CACHE_KEYS.PULL_REQUESTS_CACHE_KEY)):
            async for prs_batch in AsyncFetcher.fetch_batch(fetch_func=repo.get_pulls,
                                                    validation_func= self._filter_pull_requests,
                                                    state = state,
                                                    sort = 'created',
                                                    base = base):

                pull_requests:List[PullRequest.PullRequest] = typing.cast(List[PullRequest.PullRequest], prs_batch)
                cache.upsert(CACHE_KEYS.PULL_REQUESTS_CACHE_KEY, {pull_request.id: pull_request for pull_request in pull_requests})
                yield pull_requests
                    
        else:
            yield list(pull_request_cache.values())
            return

    async def get_team_members(self, team_slug: str) -> AsyncIterator[List[Team.Team]]:
        if (members_cache := cache.get(CACHE_KEYS.TEAM_MEMBERS_CACHE_KEY)):
            if members_slug:= members_cache.get(team_slug):
                yield list(members_slug.values())
                return

        team = await AsyncFetcher.fetch_single(self.github.org.get_team_by_slug, team_slug)
        async for members_batch in AsyncFetcher.fetch_batch(team.get_members):
            members = typing.cast(List[NamedUser.NamedUser], members_batch)
            cache.upsert(CACHE_KEYS.TEAM_MEMBERS_CACHE_KEY, {team_slug: {member for member in members}})
            yield members
        

    async def get_teams(self):
        if teams_cache := self._cache_get(CACHE_KEYS.TEAMS_CACHE_KEY):
            yield list(teams_cache.values())
        async for teams in AsyncFetcher.fetch_batch(self.github.org.get_teams):
            teams:List[Team.Team] = typing.cast(List[Team.Team], teams)
            cache.upsert(CACHE_KEYS.TEAMS_CACHE_KEY, {team.id: team for team in teams})
            yield teams

    async def get_issues(self)->AsyncIterator[List[str]]:
        async for issues_batch in AsyncFetcher.fetch_batch(
            self.repo_object.get_issues,
            validation_func=self._filter_by_timeframe
            ):
            issues = typing.cast(List[Issue.Issue], issues_batch)
            yield issues
        

github_client = GitHubClient()