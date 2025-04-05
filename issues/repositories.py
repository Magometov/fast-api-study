from repositories import BaseRepository

from issues.models import Issue

class IssueRepository(BaseRepository[Issue]):
    file_name: str = 'issues_data.json'
    model: type[Issue] = Issue