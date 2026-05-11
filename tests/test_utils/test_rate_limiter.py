"""Unit tests for Rate Limiter module."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta

from src.utils.rate_limiter import RateLimiter, RateLimitExceededError


class TestRateLimiter:
    """Test suite for RateLimiter class."""

    @pytest.mark.asyncio
    async def test_rate_limiter_initialization(self):
        """Test RateLimiter initialization."""
        limiter = RateLimiter(max_requests=20, window_seconds=60)

        assert limiter.max_requests == 20
        assert limiter.window_seconds == 60
        assert len(limiter._requests) == 0

    @pytest.mark.asyncio
    async def test_rate_limiter_allow_request(self):
        """Test allowing request within limit."""
        limiter = RateLimiter(max_requests=20, window_seconds=60)

        for i in range(20):
            assert await limiter.is_allowed(user_id=123) is True

    @pytest.mark.asyncio
    async def test_rate_limiter_deny_request(self):
        """Test denying request exceeding limit."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)

        # Make 5 requests (at limit)
        for i in range(5):
            await limiter.is_allowed(user_id=123)

        # 6th request should be denied
        assert await limiter.is_allowed(user_id=123) is False

    @pytest.mark.asyncio
    async def test_rate_limiter_different_users(self):
        """Test rate limiting for different users."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)

        # User 1 makes 3 requests
        for i in range(3):
            assert await limiter.is_allowed(user_id=1) is True

        # User 1 should be limited
        assert await limiter.is_allowed(user_id=1) is False

        # User 2 should still be allowed
        assert await limiter.is_allowed(user_id=2) is True

    @pytest.mark.asyncio
    async def test_rate_limiter_window_expiry(self):
        """Test rate limit window expiry."""
        limiter = RateLimiter(max_requests=2, window_seconds=1)

        # Make 2 requests
        assert await limiter.is_allowed(user_id=123) is True
        assert await limiter.is_allowed(user_id=123) is True

        # Should be limited
        assert await limiter.is_allowed(user_id=123) is False

        # Wait for window to expire
        await asyncio.sleep(1.1)

        # Should be allowed again
        assert await limiter.is_allowed(user_id=123) is True

    @pytest.mark.asyncio
    async def test_rate_limiter_cleanup_old_requests(self):
        """Test cleanup of old requests."""
        limiter = RateLimiter(max_requests=10, window_seconds=1)

        # Make requests for user 1
        for i in range(5):
            await limiter.is_allowed(user_id=1)

        # Make requests for user 2
        for i in range(5):
            await limiter.is_allowed(user_id=2)

        # Wait for window to expire
        await asyncio.sleep(1.1)

        # Make new request for user 3 (should trigger cleanup)
        await limiter.is_allowed(user_id=3)

        # Old requests should be cleaned up
        # Only user 3's request should remain
        assert len(limiter._requests) == 1

    @pytest.mark.asyncio
    async def test_rate_limiter_reset_user(self):
        """Test resetting rate limit for specific user."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)

        # Make 3 requests
        for i in range(3):
            await limiter.is_allowed(user_id=123)

        # Should be limited
        assert await limiter.is_allowed(user_id=123) is False

        # Reset user
        limiter.reset_user(user_id=123)

        # Should be allowed again
        assert await limiter.is_allowed(user_id=123) is True

    @pytest.mark.asyncio
    async def test_rate_limiter_reset_all(self):
        """Test resetting all rate limits."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)

        # Make requests for multiple users
        for user_id in [1, 2, 3]:
            for i in range(3):
                await limiter.is_allowed(user_id=user_id)

        # All users should be limited
        assert await limiter.is_allowed(user_id=1) is False
        assert await limiter.is_allowed(user_id=2) is False
        assert await limiter.is_allowed(user_id=3) is False

        # Reset all
        limiter.reset_all()

        # All users should be allowed again
        assert await limiter.is_allowed(user_id=1) is True
        assert await limiter.is_allowed(user_id=2) is True
        assert await limiter.is_allowed(user_id=3) is True

    @pytest.mark.asyncio
    async def test_rate_limiter_get_remaining_requests(self):
        """Test getting remaining requests for user."""
        limiter = RateLimiter(max_requests=10, window_seconds=60)

        # Initially should have 10 remaining
        assert limiter.get_remaining(user_id=123) == 10

        # Make 3 requests
        for i in range(3):
            await limiter.is_allowed(user_id=123)

        # Should have 7 remaining
        assert limiter.get_remaining(user_id=123) == 7

        # Make 7 more requests
        for i in range(7):
            await limiter.is_allowed(user_id=123)

        # Should have 0 remaining
        assert limiter.get_remaining(user_id=123) == 0

    @pytest.mark.asyncio
    async def test_rate_limiter_get_retry_after(self):
        """Test getting retry after time."""
        limiter = RateLimiter(max_requests=2, window_seconds=10)

        # Make 2 requests
        await limiter.is_allowed(user_id=123)
        await limiter.is_allowed(user_id=123)

        # Should be limited
        assert await limiter.is_allowed(user_id=123) is False

        # Get retry after time
        retry_after = limiter.get_retry_after(user_id=123)
        assert retry_after is not None
        assert 0 < retry_after <= 10

    @pytest.mark.asyncio
    async def test_rate_limiter_get_retry_after_not_limited(self):
        """Test getting retry after when not limited."""
        limiter = RateLimiter(max_requests=10, window_seconds=60)

        # Should not be limited
        retry_after = limiter.get_retry_after(user_id=123)
        assert retry_after is None

    @pytest.mark.asyncio
    async def test_rate_limiter_check_or_raise(self):
        """Test check_or_raise method."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)

        # Should not raise
        await limiter.check_or_raise(user_id=123)
        await limiter.check_or_raise(user_id=123)

        # Should raise
        with pytest.raises(RateLimitExceededError):
            await limiter.check_or_raise(user_id=123)

    @pytest.mark.asyncio
    async def test_rate_limiter_check_or_raise_custom_message(self):
        """Test check_or_raise with custom error message."""
        limiter = RateLimiter(max_requests=1, window_seconds=60)

        # Make 1 request
        await limiter.check_or_raise(user_id=123)

        # Should raise with custom message
        with pytest.raises(RateLimitExceededError, match="Rate limit exceeded"):
            await limiter.check_or_raise(user_id=123)

    @pytest.mark.asyncio
    async def test_rate_limiter_concurrent_requests(self):
        """Test rate limiting with concurrent requests."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)

        # Make concurrent requests
        tasks = [limiter.is_allowed(user_id=123) for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # First 5 should be True, rest should be False
        assert sum(results) == 5

    @pytest.mark.asyncio
    async def test_rate_limiter_sliding_window(self):
        """Test sliding window behavior."""
        limiter = RateLimiter(max_requests=3, window_seconds=2)

        # Make 3 requests
        await limiter.is_allowed(user_id=123)
        await limiter.is_allowed(user_id=123)
        await limiter.is_allowed(user_id=123)

        # Should be limited
        assert await limiter.is_allowed(user_id=123) is False

        # Wait 1 second
        await asyncio.sleep(1)

        # Still limited (window hasn't fully expired)
        assert await limiter.is_allowed(user_id=123) is False

        # Wait another 1.5 seconds (total 2.5 seconds)
        await asyncio.sleep(1.5)

        # Should be allowed now
        assert await limiter.is_allowed(user_id=123) is True

    @pytest.mark.asyncio
    async def test_rate_limiter_user_isolation(self):
        """Test that users are properly isolated."""
        limiter = RateLimiter(max_requests=1, window_seconds=60)

        # User 1 makes request
        assert await limiter.is_allowed(user_id=1) is True
        assert await limiter.is_allowed(user_id=1) is False

        # User 2 should not be affected
        assert await limiter.is_allowed(user_id=2) is True
        assert await limiter.is_allowed(user_id=2) is False

        # Reset user 1 should not affect user 2
        limiter.reset_user(user_id=1)
        assert await limiter.is_allowed(user_id=1) is True
        assert await limiter.is_allowed(user_id=2) is False

    @pytest.mark.asyncio
    async def test_rate_limiter_zero_max_requests(self):
        """Test rate limiter with zero max requests."""
        limiter = RateLimiter(max_requests=0, window_seconds=60)

        # Should always deny
        assert await limiter.is_allowed(user_id=123) is False

    @pytest.mark.asyncio
    async def test_rate_limiter_large_window(self):
        """Test rate limiter with large window."""
        limiter = RateLimiter(max_requests=100, window_seconds=3600)

        # Should allow 100 requests
        for i in range(100):
            assert await limiter.is_allowed(user_id=123) is True

        # 101st should be denied
        assert await limiter.is_allowed(user_id=123) is False
