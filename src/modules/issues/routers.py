from fastapi import APIRouter

from issues.dto import Issue
from issues.repositories import IssueRepository

router = APIRouter(prefix='/issues')

@router.post('/')
def add_issue_router(issue: Issue):
    IssueRepository().save(issue)
    return issue

@router.get('/')
def get_issues_router():
    return IssueRepository().get_all()