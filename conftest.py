import pytest
from django.test import Client
from django.test.utils import override_settings


@pytest.fixture
def client():
    """A Django test client instance."""
    return Client()


@pytest.fixture(autouse=True)
def use_static_storage():
    """Override the staticfiles storage for tests."""
    with override_settings(
        STORAGES={
            "default": {
                "BACKEND": "django.core.files.storage.FileSystemStorage",
            },
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
        }
    ):
        yield
