# Ensure the project root is on sys.path so `lib` can be imported during tests
import sys
from pathlib import Path

import pytest

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
root_str = str(PROJECT_ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

# Now that sys.path is set up, we can import database utils
from lib import database_utils


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """
    Use a temporary sqlite database file for each test and create fresh tables.
    This isolates tests from each other and from any existing local database.
    """
    db_file = tmp_path / "test_magazine.db"
    monkeypatch.setattr(database_utils, "DB_FILE", str(db_file))
    database_utils.create_tables()
    yield
