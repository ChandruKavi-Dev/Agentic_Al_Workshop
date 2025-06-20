import chromadb
from app.core.config import settings

# Initialize the persistent ChromaDB client
chroma_client = chromadb.HttpClient(
    host=settings['chromadb']['host'],
    port=settings['chromadb']['port']
)

# Get or create the collection. This is like a table in a traditional DB.
# This operation is idempotent, so it's safe to run every time.
collection = chroma_client.get_or_create_collection(
    name=settings['chromadb']['collection_name']
)

def get_chroma_collection():
    """Returns the singleton instance of the ChromaDB collection."""
    return collection