from datetime import datetime

import pytest


@pytest.fixture
def current_date() -> str:
    return datetime.now().isoformat()
