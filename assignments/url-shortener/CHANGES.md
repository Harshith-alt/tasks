## Features Implemented

- `POST /api/shorten` – Accepts a long URL and returns a short URL with a 6-character code.
- `GET /<short_code>` – Redirects to the original URL and increments the click count.
- `GET /api/stats/<short_code>` – Returns the number of clicks, original URL, and creation timestamp.
- `GET /` and `GET /api/health` – Health check endpoints.

## Security and Validation

- Input URLs are validated using a regex pattern.
- Short codes are randomly generated using alphanumeric characters.
- No external database used – all storage is in-memory (as allowed by the spec).

## Architecture

- Flask app organized in `main.py`, `models.py`, and `utils.py`.
- `models.py` contains in-memory data structure and helper functions for storing mappings and analytics.
- `utils.py` includes helper functions for generating codes and validating URLs.
- `test_basic.py` includes 6 tests: health check, shorten success, shorten failure, redirect, invalid code, and stats check.

## 🧪 Tests

- All required test cases written and pass via `pytest`.

```bash
pytest test_basic.py
```
