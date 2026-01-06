"""
Ohmyfin Python SDK Client

Official SDK for Ohmyfin API - SWIFT transaction tracking and validation.
Get your API key at https://ohmyfin.ai

Ohmyfin is previously known as TrackMySwift.
"""

import json
from typing import Any, Dict, Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class OhmyfinError(Exception):
    """Exception raised for Ohmyfin API errors."""

    def __init__(self, message: str, status_code: int = None, errors: Dict = None):
        self.message = message
        self.status_code = status_code
        self.errors = errors or {}
        super().__init__(self.message)


class Ohmyfin:
    """
    Ohmyfin API Client

    Official Python SDK for Ohmyfin API - SWIFT transaction tracking,
    validation, and correspondent banking data.

    Get your API key at https://ohmyfin.ai

    Example:
        >>> client = Ohmyfin(api_key='your-api-key')
        >>> result = client.track(
        ...     uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',
        ...     amount=10000,
        ...     date='2024-01-15',
        ...     currency='USD'
        ... )
        >>> print(result['status'])

    Attributes:
        api_key: Your Ohmyfin API key
        base_url: API base URL (default: https://ohmyfin.ai)
        timeout: Request timeout in seconds (default: 30)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://ohmyfin.ai",
        timeout: int = 30
    ):
        """
        Initialize Ohmyfin client.

        Args:
            api_key: Your Ohmyfin API key (get one at https://ohmyfin.ai)
            base_url: API base URL (default: https://ohmyfin.ai)
            timeout: Request timeout in seconds (default: 30)

        Raises:
            ValueError: If api_key is not provided
        """
        if not api_key:
            raise ValueError("API key is required. Get your API key at https://ohmyfin.ai")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _request(self, method: str, path: str, data: Dict = None) -> Dict[str, Any]:
        """Make an API request."""
        url = f"{self.base_url}{path}"

        headers = {
            "KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ohmyfin-python/1.0.0"
        }

        body = json.dumps(data).encode('utf-8') if data else None

        request = Request(url, data=body, headers=headers, method=method)

        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            try:
                error_body = json.loads(e.read().decode('utf-8'))
                raise OhmyfinError(
                    error_body.get('message', 'API request failed'),
                    e.code,
                    error_body.get('errors')
                )
            except json.JSONDecodeError:
                raise OhmyfinError(f"API request failed with status {e.code}", e.code)

    def track(
        self,
        amount: float,
        date: str,
        currency: str,
        uetr: str = None,
        ref: str = None
    ) -> Dict[str, Any]:
        """
        Track a SWIFT transaction.

        Args:
            amount: Transaction amount
            date: Transaction date (YYYY-MM-DD format)
            currency: Currency code (e.g., 'USD', 'EUR')
            uetr: UETR (Universal End-to-End Transaction Reference)
            ref: Transaction reference (required if uetr not provided)

        Returns:
            Dict containing:
                - status: Transaction status ('success', 'in progress', 'rejected', etc.)
                - lastupdate: Last update date
                - details: List of bank statuses in the payment chain
                - limits: API usage limits

        Raises:
            ValueError: If neither uetr nor ref is provided
            OhmyfinError: If the API request fails

        Example:
            >>> result = client.track(
            ...     uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',
            ...     amount=10000,
            ...     date='2024-01-15',
            ...     currency='USD'
            ... )
        """
        if not uetr and not ref:
            raise ValueError("Either uetr or ref is required")

        data = {
            "amount": amount,
            "date": date,
            "currency": currency
        }
        if uetr:
            data["uetr"] = uetr
        if ref:
            data["ref"] = ref

        return self._request("POST", "/api/track", data)

    def change(
        self,
        amount: float,
        date: str,
        currency: str,
        status: str,
        role: str,
        uetr: str = None,
        ref: str = None,
        swift: str = None,
        next_name: str = None,
        next_swift: str = None,
        message: str = None,
        details: str = None
    ) -> Dict[str, Any]:
        """
        Update/report transaction status (for financial institutions).

        Args:
            amount: Transaction amount
            date: Transaction date (YYYY-MM-DD)
            currency: Currency code
            status: Status ('in process', 'success', 'rejected', 'on hold')
            role: Role ('originator', 'beneficiary', 'intermediary', 'correspondent', 'other')
            uetr: UETR
            ref: Transaction reference (required if uetr not provided)
            swift: Your SWIFT/BIC code
            next_name: Next bank name in chain
            next_swift: Next bank SWIFT code
            message: Additional message
            details: Additional details

        Returns:
            Dict with confirmation message

        Raises:
            ValueError: If required parameters are missing
            OhmyfinError: If the API request fails

        Example:
            >>> client.change(
            ...     uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',
            ...     amount=10000,
            ...     date='2024-01-15',
            ...     currency='USD',
            ...     status='success',
            ...     role='correspondent'
            ... )
        """
        if not uetr and not ref:
            raise ValueError("Either uetr or ref is required")
        if not status or not role:
            raise ValueError("status and role are required")

        data = {
            "amount": amount,
            "date": date,
            "currency": currency,
            "status": status,
            "role": role
        }
        if uetr:
            data["uetr"] = uetr
        if ref:
            data["ref"] = ref
        if swift:
            data["swift"] = swift
        if next_name:
            data["nextName"] = next_name
        if next_swift:
            data["nextSwift"] = next_swift
        if message:
            data["message"] = message
        if details:
            data["details"] = details

        return self._request("POST", "/api/change", data)

    def validate(
        self,
        beneficiary_bic: str,
        currency: str,
        correspondent_bic: str = None,
        correspondent_account: str = None,
        beneficiary_iban: str = None,
        beneficiary_owner: str = None,
        beneficiary_country: str = None,
        beneficiary_region: str = None,
        sender_bic: str = None,
        sender_correspondent_bic: str = None
    ) -> Dict[str, Any]:
        """
        Validate a transaction before sending.

        Args:
            beneficiary_bic: Beneficiary bank SWIFT/BIC
            currency: Currency code
            correspondent_bic: Correspondent bank BIC
            correspondent_account: Correspondent account
            beneficiary_iban: Beneficiary IBAN
            beneficiary_owner: Beneficiary name
            beneficiary_country: Beneficiary country
            beneficiary_region: Beneficiary region
            sender_bic: Sender bank BIC
            sender_correspondent_bic: Sender correspondent BIC

        Returns:
            Dict containing validation status for each field:
                - beneficiary_bic: Validation result
                - beneficiary_iban: Validation result (if provided)
                - correspondent_bic: Validation result (if provided)
                - avg_business_days: Estimated business days
                - available_correspondents: List of available correspondents

        Raises:
            ValueError: If required parameters are missing
            OhmyfinError: If the API request fails

        Example:
            >>> result = client.validate(
            ...     beneficiary_bic='DEUTDEFF',
            ...     currency='EUR',
            ...     beneficiary_iban='DE89370400440532013000'
            ... )
        """
        if not beneficiary_bic or not currency:
            raise ValueError("beneficiary_bic and currency are required")

        data = {
            "beneficiary_bic": beneficiary_bic,
            "currency": currency
        }
        if correspondent_bic:
            data["correspondent_bic"] = correspondent_bic
        if correspondent_account:
            data["correspondent_account"] = correspondent_account
        if beneficiary_iban:
            data["beneficiary_iban"] = beneficiary_iban
        if beneficiary_owner:
            data["beneficiary_owner"] = beneficiary_owner
        if beneficiary_country:
            data["beneficiary_country"] = beneficiary_country
        if beneficiary_region:
            data["beneficiary_region"] = beneficiary_region
        if sender_bic:
            data["sender_bic"] = sender_bic
        if sender_correspondent_bic:
            data["sender_correspondent_bic"] = sender_correspondent_bic

        return self._request("POST", "/api/validate", data)

    def get_ssi(
        self,
        swift: str,
        currency: str
    ) -> Dict[str, Any]:
        """
        Get Standard Settlement Instructions (SSI) for a bank.

        Args:
            swift: Bank SWIFT/BIC code
            currency: Currency code

        Returns:
            Dict containing:
                - correspondents: List of correspondent banks
                - currencies: List of supported currencies
                - limits: API usage limits

        Raises:
            ValueError: If required parameters are missing
            OhmyfinError: If the API request fails

        Example:
            >>> ssi = client.get_ssi(swift='DEUTDEFF', currency='EUR')
            >>> for correspondent in ssi['correspondents']:
            ...     print(correspondent['bank'], correspondent['swift'])
        """
        if not swift or not currency:
            raise ValueError("swift and currency are required")

        data = {
            "swift": swift,
            "currency": currency
        }

        return self._request("POST", "/api/getssi", data)
