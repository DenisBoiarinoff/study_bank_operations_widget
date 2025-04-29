import pytest
from datetime import datetime

@pytest.fixture
def current_date():
    return datetime.now().isoformat()