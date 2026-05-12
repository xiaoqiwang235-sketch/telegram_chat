"""UserPreferences repository for database operations."""

from typing import List, Dict

from src.database.connection_pool import ConnectionPool
from src.repositories.base_repository import BaseRepository


class UserPreferencesRepository(BaseRepository):
    """Repository for user preferences operations."""

    async def create(
        self, user_id: int, style_id: int, language: str = "en"
    ) -> bool:
        """Create new user preferences.

        Args:
            user_id: User ID
            style_id: Preferred conversation style ID
            language: Preferred language code

        Returns:
            True if created successfully
        """
        query = """
            INSERT INTO user_preferences (user_id, style_id, language)
            VALUES (%s, %s, %s)
        """
        params = (user_id, style_id, language)

        await self._execute_write(query, params)
        return True

    async def get_by_id(self, pref_id: int) -> Dict | None:
        """Get user preferences by ID.

        Args:
            pref_id: Preference ID to search for

        Returns:
            Dictionary with preferences if found, None otherwise
        """
        query = """
            SELECT id, user_id, style_id, language
            FROM user_preferences
            WHERE id = %s
        """
        result = await self._execute_query_one(query, (pref_id,))

        if result:
            return self._row_to_dict(result)
        return None

    async def get_by_user_id(self, user_id: int) -> Dict | None:
        """Get user preferences by user ID.

        Args:
            user_id: User ID to search for

        Returns:
            Dictionary with preferences if found, None otherwise
        """
        query = """
            SELECT id, user_id, style_id, language
            FROM user_preferences
            WHERE user_id = %s
        """
        result = await self._execute_query_one(query, (user_id,))

        if result:
            return self._row_to_dict(result)
        return None

    async def update(
        self, user_id: int, style_id: int, language: str = "en"
    ) -> bool:
        """Update user preferences.

        Args:
            user_id: User ID to update
            style_id: New preferred conversation style ID
            language: New preferred language code

        Returns:
            True if updated successfully, False if not found
        """
        query = """
            UPDATE user_preferences
            SET style_id = %s, language = %s
            WHERE user_id = %s
        """
        params = (style_id, language, user_id)

        rows_affected = await self._execute_write(query, params)
        return rows_affected > 0

    async def delete(self, user_id: int) -> bool:
        """Delete user preferences.

        Args:
            user_id: User ID to delete preferences for

        Returns:
            True if deleted, False if not found
        """
        query = "DELETE FROM user_preferences WHERE user_id = %s"
        rows_affected = await self._execute_write(query, (user_id,))
        return rows_affected > 0

    async def exists(self, user_id: int) -> bool:
        """Check if user preferences exist.

        Args:
            user_id: User ID to check

        Returns:
            True if preferences exist, False otherwise
        """
        query = "SELECT 1 FROM user_preferences WHERE user_id = %s"
        result = await self._execute_query_one(query, (user_id,))
        return result is not None

    async def get_all(self) -> List[Dict]:
        """Get all user preferences.

        Returns:
            List of dictionaries with user preferences
        """
        query = """
            SELECT id, user_id, style_id, language
            FROM user_preferences
            ORDER BY user_id
        """
        results = await self._execute_query(query)
        return [self._row_to_dict(row) for row in results]

    async def count(self) -> int:
        """Count total number of user preferences.

        Returns:
            Total user preferences count
        """
        query = "SELECT COUNT(*) FROM user_preferences"
        result = await self._execute_query_one(query)
        if result:
            return result[0]
        return 0

    async def create_or_update(
        self, user_id: int, style_id: int, language: str = "en"
    ) -> bool:
        """Create new user preferences or update if exists.

        Args:
            user_id: User ID
            style_id: Preferred conversation style ID
            language: Preferred language code

        Returns:
            True if created or updated successfully
        """
        existing_prefs = await self.get_by_user_id(user_id)

        if existing_prefs:
            return await self.update(user_id, style_id, language)
        else:
            return await self.create(user_id, style_id, language)

    async def get_by_style_id(self, style_id: int) -> List[Dict]:
        """Get user preferences by style ID.

        Args:
            style_id: Style ID to filter by

        Returns:
            List of dictionaries with user preferences
        """
        query = """
            SELECT id, user_id, style_id, language
            FROM user_preferences
            WHERE style_id = %s
            ORDER BY user_id
        """
        results = await self._execute_query(query, (style_id,))
        return [self._row_to_dict(row) for row in results]

    def _row_to_dict(self, row: tuple) -> Dict:
        """Convert database row to dictionary.

        Args:
            row: Database row tuple

        Returns:
            Dictionary with preferences
        """
        return {
            "id": row[0],
            "user_id": row[1],
            "style_id": row[2],
            "language": row[3],
        }
