from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    password: str
    role: str       # visitor or staff
    room_type: Optional[str] = None # suite or basic
    room_id: Optional[int] = None

class UserManager:
    def __init__(self):
        self._users: dict[str, User] = {}

    def add_user(self, user: User):
        self._users[user.username] = user

    def authenticate(self, username: str, password: str):
        user = self._users.get(username)
        if user and user.password == password:
            return user
        return None