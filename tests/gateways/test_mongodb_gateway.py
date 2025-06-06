import mongomock
import pytest

from gateways import mongodb_gateway

@pytest.fixture
def gateway():
    client = mongomock.MongoClient()
    gateway = mongodb_gateway.MongoDBGateway(
        uri="mongodb://localhost:27017/",
        database_name="testdb",
        collection_name="testcollection",
        client=client
    )
    yield gateway
    gateway.close()

def test_add(gateway):
    documents = [
        {"title": "Doc 1", "content": "Test 1"},
        {"title": "Doc 2", "content": "Test 2"}
    ]
    inserted_ids = gateway.add(documents)
    assert len(inserted_ids) == 2

    all_docs = gateway.get({})
    assert len(all_docs) == 2
    titles = [doc["title"] for doc in all_docs]
    assert "Doc 1" in titles
    assert "Doc 2" in titles

def test_add_empty(gateway):
    inserted_ids = gateway.add([])
    assert inserted_ids == []

def test_get(gateway):
    documents = [
        {"title": "Doc 1", "content": "Test 1"},
        {"title": "Doc 2", "content": "Test 2"}
    ]
    gateway.add(documents)
    result = gateway.get({"title": "Doc 1"})
    assert len(result) == 1
    assert result[0]["title"] == "Doc 1"

def test_get_no_query(gateway):
    documents = [
        {"title": "Doc 1", "content": "Test 1"},
        {"title": "Doc 2", "content": "Test 2"}
    ]
    gateway.add(documents)
    result = gateway.get({})
    assert len(result) == 2

def test_connection_closes(gateway):
    gateway.close()
