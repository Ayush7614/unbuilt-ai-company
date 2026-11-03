# Local Development Installation

1. Install Python 3.12 or newer.
2. Change into `services/api`.
3. Create and activate a virtual environment.
4. Install `python -m pip install -e '.[dev]'`.
5. Start `uvicorn app.main:app --reload`.
6. Open `http://127.0.0.1:8000/docs`.
7. Run `python -m pytest -q` to execute the API test suite.

The current local setup uses SQLite by default. PostgreSQL connectivity is supported through SQLAlchemy's `DATABASE_URL` setting, but a PostgreSQL service/container and migration workflow are not yet included in this foundation milestone.
