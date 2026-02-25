import os
import sys

# Get the project root directory
current_file = os.path.abspath(__file__)
database_dir = os.path.dirname(current_file)
backend_dir = os.path.dirname(database_dir)
project_root = os.path.dirname(backend_dir)

# Add project root to sys.path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    chromadb = None

try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    OpenAIEmbeddings = None

def get_vector_db():
    """Initializes and returns the ChromaDB client."""
    if chromadb is None:
        raise ImportError("chromadb is not installed. Run: pip install chromadb")
    
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Check if OpenAI embeddings are available
    if OpenAIEmbeddings is not None:
        try:
            openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key="your-api-key",  # Should come from .env
                model_name="text-embedding-3-small"
            )
        except Exception:
            # If OpenAI API key is not set, use default embedding
            openai_ef = None
    else:
        openai_ef = None
    
    collection = client.get_or_create_collection(
        name="medical_base",
        embedding_function=openai_ef
    )
    return collection

def query_medical_rag(query: str):
    """Placeholder for RAG query logic."""
    # In a real implementation, this would query the vector database
    # For now, return a mock response
    return "Based on medical documentation, the symptoms suggest early stage fatigue. Recommended rest."
