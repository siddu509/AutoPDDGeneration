"""
Middleware for the PDD Generator API.

This module contains custom middleware for rate limiting, request logging,
and other cross-cutting concerns.
"""

import time
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import get_logger

# Get module logger
logger = get_logger(__name__)


# Initialize rate limiter
# Uses IP address as the unique identifier
limiter = Limiter(key_func=get_remote_address)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses.

    Logs the following information for each request:
    - HTTP method and path
    - Client IP address
    - Request processing time
    - Response status code

    This middleware helps with debugging, monitoring, and audit trails.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler in the chain

        Returns:
            HTTP response from the route handler
        """
        # Start timer
        start_time = time.time()

        # Extract request details
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"

        # Log request
        logger.info(f"➡️  {method} {url} from {client_host}")

        # Process request
        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log response
            logger.info(
                f"⬅️  {method} {url} - Status: {response.status_code} "
                f"- Time: {process_time:.3f}s"
            )

            # Add timing header to response (useful for debugging)
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # Calculate processing time for failed requests
            process_time = time.time() - start_time

            # Log error
            logger.error(
                f"❌ {method} {url} - Error: {str(e)} - Time: {process_time:.3f}s"
            )

            # Re-raise the exception for FastAPI to handle
            raise


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom handler for rate limit exceeded errors.

    This function is called when a client exceeds the rate limit.
    It logs the event and returns a friendly error message.

    Args:
        request: The HTTP request that exceeded the rate limit
        exc: The RateLimitExceeded exception

    Returns:
        JSON response with error details
    """
    client_host = request.client.host if request.client else "unknown"

    logger.warning(
        f"⚠️  Rate limit exceeded for {client_host} accessing {request.url.path}"
    )

    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=429,
        content={
            "detail": (
                f"Rate limit exceeded: {exc.detail}. "
                "Please slow down your requests."
            ),
            "error_code": "RATE_LIMIT_EXCEEDED",
            "retry_after": "60"  # Suggest waiting 60 seconds
        },
        headers={
            "Retry-After": "60",
            "X-RateLimit-Limit": str(exc.detail),
        },
    )
