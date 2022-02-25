import pytest
import src.settings as settings
import src.utilities as utilities

@pytest.fixture
def url():
    return settings.endpoint


@pytest.fixture
def timeout():
    return settings.timeout


@pytest.fixture
def retries():
    return settings.retries


@pytest.fixture
def client(url, timeout, retries):
    return utilities.generate_client(url=url,
                                     timeout=timeout,
                                     retries=retries)


