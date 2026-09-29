"""
db.py
-----

This defines a mock db object that can create and delete users.

The responsibility of this module is just to store and retrieve users.

It does not handle any user interaction or business logic.
"""


class DB:
    class UniqueConstraintError(Exception):
        pass

    def __init__(self, connection_str):
        self.users = set()

    def insert(self, username: str):
        """Create a new user in the database. If the user already exists,
        raise UniqueConstraintError."""
        if username in self.users:
            raise self.UniqueConstraintError(f"user {username} already exists.")
        self.users.add(username)

    def delete_user(self, username: str) -> bool:
        """Delete a user from the database. If the user does not exist, do nothing.
        Returns True if the user was deleted, False otherwise."""
        try:
            self.users.remove(username)
            return True
        except KeyError:
            return False

    def list_users(self) -> set[str]:
        return self.users
