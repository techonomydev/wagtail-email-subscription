from io import StringIO

import pytest
from django.core import management


@pytest.mark.django_db
def test_has_all_migrations():
    output = StringIO()
    management.call_command(
        "makemigrations", verbosity=1, interactive=False, stdout=output
    )
    output.seek(0)
    output = output.read().strip()
    assert "No changes detected" in output
