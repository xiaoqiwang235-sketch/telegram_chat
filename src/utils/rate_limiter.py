"""Rate limiting utilities."""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, Deque


class RateLimitExceededError(Exception):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None):
        """Initialize rate limit exceeded error.

        Args:
            message: Error message
            retry_after: Seconds until user can retry
        """
        super().__init__(message)
        self.retry_after = retry_after


@dataclass
class RateLimiter:
    """Sliding window rate limiter.

    Attributes:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        _requests: Dictionary of user request timestamps
    """

    max_requests: int
    window_seconds: int
    _requests: Dict[int, Deque[float]] = defaultdict(deque)

    async def is_allowed(self, user_id: int) -> bool:
        """Check if request is allowed for user.

        Args:
            user_id: User ID to check

        Returns:
            True if request is allowed, False otherwise
        """
        current_time = time.time()

        # Clean up old requests outside the window
        self._cleanup_old_requests(user_id, current_time)

        # Check if under limit
        if len(self._requests[user_id]) < self.max_requests:
            self._requests[user_id].append(current_time)
            return True

        return False

    def _cleanup_old_requests(self, user_id: int, current_time: float) -> None:
        """Remove requests outside the time window.

        Args:
            user_id: User ID to cleanup
            current_time: Current timestamp
        """
        window_start = current_time - self.window_seconds

        # Remove old requests
        while self._requests[user_id] and self._requests[user_id][0] < window_start:
            self._requests[user_id].popleft()

        # Clean up empty queues to save memory
        if not self._requests[user_id]:
            del self._requests[user_id]

    def reset_user(self, user_id: int) -> None:
        """Reset rate limit for specific user.

        Args:
            user_id: User ID to reset
        """
        if user_id in self._requests:
            del self._requests[user_id]

    def reset_all(self) -> None:
        """Reset all rate limits."""
        self._requests.clear()

    def get_remaining(self, user_id: int) -> int:
        """Get remaining requests for user.

        Args:
            user_id: User ID to check

        Returns:
            Number of remaining requests
        """
        current_time = time.time()
        self._cleanup_old_requests(user_id, current_time)

        if user_id not in self._requests:
            return self.max_requests

        return max(0, self.max_requests - len(self._requests[user_id]))

    def get_retry_after(self, user_id: int) -> int | None:
        """Get seconds until user can make next request.

        Args:
            user_id: User ID to check

        Returns:
            Seconds until retry, or None if not limited
        """
        current_time = time.time()
        self._cleanup_old_requests(user_id, current_time)

        if user_id not in self._requests:
            return None

        if len(self._requests[user_id]) < self.max_requests:
            return None

        # Calculate when oldest request will expire
        oldest_request = self._requests[user_id][0]
        retry_after = int(oldest_request + self.window_seconds - current_time)

        return max(0, retry_after)

    async def check_or_raise(self, user_id: int) -> None:
        """Check if request is allowed, raise exception if not.

        Args:
            user_id: User ID to check

        Raises:
            RateLimitExceededError: If rate limit exceeded
        """
        if not await self.is_allowed(user_id):
            retry_after = self.get_retry_after(user_id)
            raise RateLimitExceededError(
                f"Rate limit exceeded for user {user_id}. "
                f"Maximum {self.max_requests} requests per {self.window_seconds} seconds.",
                retry_after=retry_after,
            )
