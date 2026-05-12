"""User repository for database operations."""

from typing import List

from src.database.connection_pool import ConnectionPool
from src.models.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Repository for User model operations."""

    async def create(self, user: User) -> User:
        """Create a new user.

        Args:
            user: User to create

        Returns:
            Created user
        """
        query = """
            INSERT INTO users (user_id, username, first_name, last_name, language_code, is_bot, is_premium)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user.user_id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code,
            user.is_bot,
            user.is_premium,
        )

        await self._execute_write(query, params)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID to search for

        Returns:
            User if found, None otherwise
        """
        query = """
            SELECT user_id, username, first_name, last_name, language_code, is_bot, is_premium
            FROM users
            WHERE user_id = %s
        """
        result = await self._execute_query_one(query, (user_id,))

        if result:
            return self._row_to_user(result)
        return None

    async def get_by_username(self, username: str) -> User | None:
        """Get user by username.

        Args:
            username: Username to search for

        Returns:
            User if found, None otherwise
        """
        query = """
            SELECT user_id, username, first_name, last_name, language_code, is_bot, is_premium
            FROM users
            WHERE username = %s
        """
        result = await self._execute_query_one(query, (username,))

        if result:
            return self._row_to_user(result)
        return None

    async def update(self, user: User) -> User:
        """Update an existing user.

        Args:
            user: User to update

        Returns:
            Updated user
        """
        query = """
            UPDATE users
            SET username = %s, first_name = %s, last_name = %s, language_code = %s, is_bot = %s, is_premium = %s
            WHERE user_id = %s
        """
        params = (
            user.username,
            user.first_name,
            user.last_name,
            user.language_code,
            user.is_bot,
            user.is_premium,
            user.user_id,
        )

        await self._execute_write(query, params)
        return user

    async def delete(self, user_id: int) -> bool:
        """Delete a user.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if not found
        """
        query = "DELETE FROM users WHERE user_id = %s"
        rows_affected = await self._execute_write(query, (user_id,))
        return rows_affected > 0

    async def exists(self, user_id: int) -> bool:
        """Check if user exists.

        Args:
            user_id: User ID to check

        Returns:
            True if user exists, False otherwise
        """
        query = "SELECT 1 FROM users WHERE user_id = %s"
        result = await self._execute_query_one(query, (user_id,))
        return result is not None

    async def get_all(self) -> List[User]:
        """Get all users.

        Returns:
            List of all users
        """
        query = """
            SELECT user_id, username, first_name, last_name, language_code, is_bot, is_premium
            FROM users
            ORDER BY user_id
        """
        results = await self._execute_query(query)
        return [self._row_to_user(row) for row in results]

    async def count(self) -> int:
        """Count total number of users.

        Returns:
            Total user count
        """
        query = "SELECT COUNT(*) FROM users"
        result = await self._execute_query_one(query)
        if result:
            return result[0]
        return 0

    async def create_or_update(self, user: User) -> User:
        """Create a new user or update if exists.

        Args:
            user: User to create or update

        Returns:
            Created or updated user
        """
        existing_user = await self.get_by_id(user.user_id)

        if existing_user:
            return await self.update(user)
        else:
            return await self.create(user)

    def _row_to_user(self, row: tuple) -> User:
        """Convert database row to User object.

        Args:
            row: Database row tuple

        Returns:
            User instance
        """
        return User(
            user_id=row[0],
            username=row[1],
            first_name=row[2],
            last_name=row[3],
            language_code=row[4],
            is_bot=bool(row[5]),
            is_premium=bool(row[6]),
        )
