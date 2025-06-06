from gateways import doc_gateway
from pymongo import MongoClient

class MongoDBGateway(doc_gateway.DocumentGateway):
    """
    A simple MongoDB gateway to insert and retrieve documents.
    """

    def __init__(self, database_name: str, collection_name: str, uri: str = "", client: MongoClient = None):
        """
        Initialize the MongoDBGateway.

        :param database_name: Name of the target database.
        :param collection_name: Name of the target collection.
        :param uri: MongoDB connection URI. If provided, client is ignored.
        :param client: Optional MongoClient instance. If provided, uri is ignored.
        """
        if client:
            self.client = client
        else:
            self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def add(self, documents: list[dict]) -> list[str]:
        """
        Inserts multiple documents into the collection.

        :param documents: List of Python dictionaries.
        :return: List of inserted document IDs as strings.
        """
        if not documents:
            print("No documents to insert.")
            return []

        result = self.collection.insert_many(documents)
        return [str(doc_id) for doc_id in result.inserted_ids]

    def get(self, query: dict) -> list[dict]:
        """
        Retrieves documents from the collection.

        :param query: Query to filter documents.
        :return: List of documents matching the query.
        """
        documents = list(self.collection.find(query))
        # Convert ObjectId to string for easier handling
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return documents

    def close(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
