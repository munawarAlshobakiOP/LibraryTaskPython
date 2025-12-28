from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface


class SQLUserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        Args:
            username (str): The username of the user.
        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user: User) -> User:
        """
        Create a new user in the database.
        Args:
            user (User): The User object to create.
        Returns:
            User: The newly created User object with updated fields (e.g., ID).
        """
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
