from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface


class UserService:
    def __init__(self, repo: UserRepositoryInterface):
        """
        Initialize the UserService with the given repository.
        """
        self.repo = repo

    def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.
        Args:
            username (str): The username of the user.
        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        return self.repo.get_by_username(username)

    def create_user(self, username: str, password: str):
        """
        Create a new user with the given username and password.
        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
        Returns:
            User: The newly created User object.
        """
        new_user = User(username=username, password_hash=get_password_hash(password))
        return self.repo.create(new_user)
