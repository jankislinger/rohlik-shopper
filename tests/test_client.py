import pytest

from rohlik_shopper.client import RohlikClient
from rohlik_shopper.credentials import RohlikCredentials
from rohlik_shopper.session import RohlikSession


@pytest.fixture
def client() -> RohlikClient:
    cred = RohlikCredentials("foo", "bar")
    return RohlikClient(cred, RohlikSession())



def test_search(client: RohlikClient):
    response = client.search("rohlík")
    print(response)