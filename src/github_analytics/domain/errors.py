class RepositoryNotFoundError(Exception):
    def __init__(self, full_name: str) -> None:
        super().__init__(f"Repository not found: {full_name}")
        self.full_name = full_name


class GitHubApiError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code


class GitHubRateLimitError(GitHubApiError):
    pass
