from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface
from app.core.security import get_password_hash


class UserService:
    def __init__(self, repo: UserRepositoryInterface):
        self.repo = repo

    def get_user_by_username(self, username: str):
        return self.repo.get_by_username(username)

    def create_user(self, username: str, password: str):
        new_user = User(username=username, password_hash=get_password_hash(password))
        return self.repo.create(new_user)
