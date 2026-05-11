"""GroupSettings repository for database operations."""

from typing import List

from src.database.connection_pool import ConnectionPool
from src.models.group_settings import GroupSettings
from src.repositories.base_repository import BaseRepository


class GroupSettingsRepository(BaseRepository):
    """Repository for GroupSettings model operations."""

    async def create(self, settings: GroupSettings) -> GroupSettings:
        """Create new group settings.

        Args:
            settings: Group settings to create

        Returns:
            Created group settings
        """
        query = """
            INSERT INTO group_settings (group_id, style_id, welcome_message, auto_reply_enabled, language)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            settings.group_id,
            settings.style_id,
            settings.welcome_message,
            settings.auto_reply_enabled,
            settings.language,
        )

        await self._execute_write(query, params)
        return settings

    async def get_by_id(self, group_id: int) -> GroupSettings | None:
        """Get group settings by ID.

        Args:
            group_id: Group ID to search for

        Returns:
            GroupSettings if found, None otherwise
        """
        query = """
            SELECT group_id, style_id, welcome_message, auto_reply_enabled, language
            FROM group_settings
            WHERE group_id = %s
        """
        result = await self._execute_query_one(query, (group_id,))

        if result:
            return self._row_to_group_settings(result)
        return None

    async def update(self, settings: GroupSettings) -> GroupSettings:
        """Update existing group settings.

        Args:
            settings: Group settings to update

        Returns:
            Updated group settings
        """
        query = """
            UPDATE group_settings
            SET style_id = %s, welcome_message = %s, auto_reply_enabled = %s, language = %s
            WHERE group_id = %s
        """
        params = (
            settings.style_id,
            settings.welcome_message,
            settings.auto_reply_enabled,
            settings.language,
            settings.group_id,
        )

        await self._execute_write(query, params)
        return settings

    async def delete(self, group_id: int) -> bool:
        """Delete group settings.

        Args:
            group_id: Group ID to delete

        Returns:
            True if deleted, False if not found
        """
        query = "DELETE FROM group_settings WHERE group_id = %s"
        rows_affected = await self._execute_write(query, (group_id,))
        return rows_affected > 0

    async def exists(self, group_id: int) -> bool:
        """Check if group settings exist.

        Args:
            group_id: Group ID to check

        Returns:
            True if group settings exist, False otherwise
        """
        query = "SELECT 1 FROM group_settings WHERE group_id = %s"
        result = await self._execute_query_one(query, (group_id,))
        return result is not None

    async def get_all(self) -> List[GroupSettings]:
        """Get all group settings.

        Returns:
            List of all group settings
        """
        query = """
            SELECT group_id, style_id, welcome_message, auto_reply_enabled, language
            FROM group_settings
            ORDER BY group_id
        """
        results = await self._execute_query(query)
        return [self._row_to_group_settings(row) for row in results]

    async def count(self) -> int:
        """Count total number of group settings.

        Returns:
            Total group settings count
        """
        query = "SELECT COUNT(*) FROM group_settings"
        result = await self._execute_query_one(query)
        if result:
            return result[0]
        return 0

    async def create_or_update(self, settings: GroupSettings) -> GroupSettings:
        """Create new group settings or update if exists.

        Args:
            settings: Group settings to create or update

        Returns:
            Created or updated group settings
        """
        existing_settings = await self.get_by_id(settings.group_id)

        if existing_settings:
            return await self.update(settings)
        else:
            return await self.create(settings)

    async def get_by_style_id(self, style_id: int) -> List[GroupSettings]:
        """Get group settings by style ID.

        Args:
            style_id: Style ID to filter by

        Returns:
            List of group settings with the specified style
        """
        query = """
            SELECT group_id, style_id, welcome_message, auto_reply_enabled, language
            FROM group_settings
            WHERE style_id = %s
            ORDER BY group_id
        """
        results = await self._execute_query(query, (style_id,))
        return [self._row_to_group_settings(row) for row in results]

    def _row_to_group_settings(self, row: tuple) -> GroupSettings:
        """Convert database row to GroupSettings object.

        Args:
            row: Database row tuple

        Returns:
            GroupSettings instance
        """
        return GroupSettings(
            group_id=row[0],
            style_id=row[1],
            welcome_message=row[2],
            auto_reply_enabled=bool(row[3]),
            language=row[4],
        )
