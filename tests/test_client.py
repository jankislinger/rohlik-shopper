import pytest

from rohlik_shopper.client import RohlikClient
from rohlik_shopper.credentials import RohlikCredentials
from rohlik_shopper.session import RohlikSession


@pytest.fixture
def client() -> RohlikClient:
    cred = RohlikCredentials.from_environ(use_dotenv=True)
    return RohlikClient(cred, RohlikSession())



def test_search(client: RohlikClient):
    response = client.search("rohlík")
    print(response)

def test_adding_item(client: RohlikClient):
    response = client.add_items(1423422, 2)
    print(response)
