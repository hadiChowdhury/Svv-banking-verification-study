# Baseline Execution Record

## Environment

- Operating system: macOS
- Python: 3.10.20
- Virtual environment: `.venv`
- pip: 24.0
- Subject system: `saadmk11/banking-system`
- Pinned upstream commit:
  `9c3ee3eea75030280405506c62d968d646981c05`

## Dependency Installation

The original upstream dependencies were installed without modifying the
subject system's requirements.

Celery 4.4.7 contains legacy package metadata that is rejected by pip 24.1
and later. Therefore, pip 24.0 was used to reproduce the original dependency
configuration.

## Django System Check

Command:

```bash
python manage.py check
```
