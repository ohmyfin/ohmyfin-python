# Ohmyfin Python SDK

[![PyPI version](https://img.shields.io/pypi/v/ohmyfin.svg)](https://pypi.org/project/ohmyfin/)
[![Python versions](https://img.shields.io/pypi/pyversions/ohmyfin.svg)](https://pypi.org/project/ohmyfin/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [Ohmyfin API](https://ohmyfin.ai) - SWIFT transaction tracking, validation, and correspondent banking data.

**Ohmyfin** (previously known as TrackMySwift) provides real-time SWIFT payment tracking, transaction validation, and Standard Settlement Instructions (SSI) data for financial institutions and businesses.

## Features

- **Transaction Tracking** - Track SWIFT payments in real-time using UETR or reference
- **Payment Validation** - Validate transactions before sending (BIC, IBAN, sanctions)
- **SSI Data** - Access Standard Settlement Instructions and correspondent banking data
- **Status Updates** - Report transaction status (for financial institutions)

## Installation

```bash
pip install ohmyfin
```

## Quick Start

Get your API key at [https://ohmyfin.ai](https://ohmyfin.ai)

```python
from ohmyfin import Ohmyfin

client = Ohmyfin(api_key='your-api-key')

# Track a transaction
result = client.track(
    uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',
    amount=10000,
    date='2024-01-15',
    currency='USD'
)

print(result['status'])  # 'success', 'in progress', 'rejected', etc.
```

## API Reference

### Constructor

```python
client = Ohmyfin(
    api_key='your-api-key',        # Required - get yours at https://ohmyfin.ai
    base_url='https://ohmyfin.ai',  # Optional
    timeout=30                      # Optional - request timeout in seconds
)
```

### track()

Track a SWIFT transaction by UETR or reference.

```python
result = client.track(
    uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',  # or use 'ref'
    amount=10000,
    date='2024-01-15',
    currency='USD'
)
```

**Response:**
```python
{
    'status': 'in progress',  # 'success', 'rejected', 'on hold', 'unknown'
    'lastupdate': '2024-01-15',
    'details': [
        {
            'id': 0,
            'bank': 'JP MORGAN CHASE',
            'swift': 'CHASUS33',
            'status': 'success',
            'reason': '',
            'route': 'confirmed'
        }
    ],
    'limits': {'daily': 100, 'monthly': 1000, 'annual': 10000}
}
```

### validate()

Validate a transaction before sending.

```python
result = client.validate(
    beneficiary_bic='DEUTDEFF',
    currency='EUR',
    beneficiary_iban='DE89370400440532013000',
    correspondent_bic='COBADEFF',  # Optional
    sender_bic='CHASUS33'          # Optional
)
```

**Response:**
```python
{
    'beneficiary_bic': {'status': 'ok'},
    'beneficiary_iban': {'status': 'ok'},
    'correspondent_bic': {
        'status': 'warning',
        'details': 'Not the preferred correspondent'
    },
    'avg_business_days': 1,
    'available_correspondents': [
        {'corresBIC': 'COBADEFF', 'is_preferred': True}
    ]
}
```

### get_ssi()

Get Standard Settlement Instructions for a bank.

```python
ssi = client.get_ssi(swift='DEUTDEFF', currency='EUR')
```

**Response:**
```python
{
    'correspondents': [
        {
            'id': 1,
            'bank': 'COMMERZBANK AG',
            'swift': 'COBADEFF',
            'currency': 'EUR',
            'account': '400886700401',
            'is_preferred': True
        }
    ],
    'currencies': ['EUR', 'USD', 'GBP']
}
```

### change()

Report transaction status updates (for financial institutions).

```python
client.change(
    uetr='97ed4827-7b6f-4491-a06f-b548d5a7512d',
    amount=10000,
    date='2024-01-15',
    currency='USD',
    status='success',     # 'in process', 'success', 'rejected', 'on hold'
    role='correspondent'  # 'originator', 'beneficiary', 'intermediary', 'correspondent', 'other'
)
```

## Error Handling

```python
from ohmyfin import Ohmyfin, OhmyfinError

try:
    result = client.track(...)
except OhmyfinError as e:
    print(e.status_code)  # HTTP status code
    print(e.errors)       # Validation errors
    print(e.message)      # Error message
```

## Links

- **Website:** [https://ohmyfin.ai](https://ohmyfin.ai)
- **API Documentation:** [https://ohmyfin.ai/api-documentation](https://ohmyfin.ai/api-documentation)
- **Get API Key:** [https://ohmyfin.ai](https://ohmyfin.ai)
- **Support:** support@ohmyfin.ai

## About Ohmyfin

[Ohmyfin](https://ohmyfin.ai) (previously known as TrackMySwift) is a software platform providing transaction tracking, validation, and correspondent banking reference data. We serve individuals, businesses, and financial institutions worldwide.

**We do not provide any financial services.**

## Trademarks

SWIFT, BIC, UETR, and related terms are trademarks owned by S.W.I.F.T. SC, headquartered at Avenue Adele 1, 1310 La Hulpe, Belgium. Ohmyfin is not affiliated with S.W.I.F.T. SC. Other product and company names mentioned herein may be trademarks of their respective owners.

## License

MIT License - see [LICENSE](LICENSE) file.
