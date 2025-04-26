import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_check(client):
    """Test that the health check endpoint returns a 200 status code."""
    url = reverse("health_check")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
