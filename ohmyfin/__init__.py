"""
Ohmyfin Python SDK

Official SDK for Ohmyfin API - SWIFT transaction tracking and validation.

Get your API key at https://ohmyfin.ai

Example:
    >>> from ohmyfin import Ohmyfin
    >>> client = Ohmyfin(api_key='your-api-key')
    >>> result = client.track(
    ...     uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',
    ...     amount=10000,
    ...     date='2024-01-15',
    ...     currency='USD'
    ... )
    >>> print(result['status'])
"""

from .client import Ohmyfin, OhmyfinError

__version__ = "1.0.0"
__all__ = ["Ohmyfin", "OhmyfinError"]
