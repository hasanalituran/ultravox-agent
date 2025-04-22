from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize dotenv to load environment variables
load_dotenv()

class FaissVectorStore:
    faiss_vector_store = None

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def create_vector_store(self):
        if self.faiss_vector_store is None:
            self.faiss_vector_store = create_vector_store(self.embeddings)
        return self.faiss_vector_store
    

def create_vector_store(embeddings) -> FAISS:
    # Determine the absolute path to the data file relative to this script
    script_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(script_dir, "data", "test-mobile-mechanics.txt")
    
    logger.info(f"Loading documents from: {data_file_path}")
    loader = TextLoader(data_file_path) # Use absolute path
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    vector_store = None

    try:
        vector_store = FAISS.load_local("faiss_vector_store", embeddings=embeddings, allow_dangerous_deserialization=True)
        print("Loaded FAISS index from local storage")
    except RuntimeError:
        vector_store = FAISS.from_documents(all_splits, embeddings)
        vector_store.save_local("faiss_vector_store")
        print("Saved FAISS index to local storage")

    return vector_store
