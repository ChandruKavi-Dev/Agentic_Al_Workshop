# rag_pipeline.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Configure the Gemini API key
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

DATA_PATH = "data/"
VECTOR_DB_PATH = "vector_db/faiss_index"

def create_vector_db():
    """
    Creates and persists a FAISS vector database from documents in the data directory.
    """
    print("Loading documents from 'data/' directory...")
    # Make sure the data directory exists
    if not os.path.exists(DATA_PATH) or not os.listdir(DATA_PATH):
        print(f"Error: The '{DATA_PATH}' directory is empty or does not exist.")
        print("Please add your markdown data files to it before running.")
        return

    loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=TextLoader, show_progress=True)
    documents = loader.load()
    if not documents:
        raise ValueError("No markdown documents found in the data directory.")

    print(f"Loaded {len(documents)} documents. Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    if not chunks:
        raise ValueError("Document splitting resulted in no chunks.")
    
    print(f"Split into {len(chunks)} chunks. Generating embeddings and creating FAISS index...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Ensure the target directory exists before saving
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vector_db = FAISS.from_documents(chunks, embedding=embeddings)

    print(f"Saving FAISS index to {VECTOR_DB_PATH}...")
    vector_db.save_local(VECTOR_DB_PATH)
    print("Vector DB created successfully.")

def get_retriever():
    """
    Loads the persisted FAISS index and returns a retriever object.
    If the index does not exist, it creates it first.
    """
    # --- THIS IS THE CORRECTED LOGIC ---
    # Check for the actual index file, not just the directory.
    index_path = os.path.join(VECTOR_DB_PATH, "index.faiss")

    if not os.path.exists(index_path):
        print("FAISS index not found. Running creation process...")
        create_vector_db()

    print("Loading existing FAISS index...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # It's now safe to load because we've ensured it exists.
    vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

    return vector_db.as_retriever(search_kwargs={'k': 5})

if __name__ == '__main__':
    # This allows you to build the DB initially by running: python rag_pipeline.py
    print("Initializing RAG pipeline...")
    retriever = get_retriever()
    print("Retriever is ready.")
    # You can add a test query here if you want
    # results = retriever.invoke("What are some fellowship options?")
    # print("Test query results:", results)