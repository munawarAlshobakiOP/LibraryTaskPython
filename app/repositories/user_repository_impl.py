from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface


class SQLUserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
