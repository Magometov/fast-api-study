from users.models import User

from repositories import BaseRepository

class UserRepository(BaseRepository[User]):
    file_name: str = 'users_data.json'
    model: type[User] = User