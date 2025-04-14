from src.core.types.repositories import BaseRepository

from issues.dto import Issue

class IssueRepository(BaseRepository[Issue]):
    file_name: str = 'issues_data.json'
    model: type[Issue] = Issue