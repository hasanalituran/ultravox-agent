from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
import logging
from langchain_community.document_loaders import S3FileLoader

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
    vector_store = None

    try:
        vector_store = FAISS.load_local("faiss_vector_store", embeddings=embeddings, allow_dangerous_deserialization=True)
        print("Loaded FAISS index from local storage")
    except RuntimeError:
        # s3://ragagentbucket/agent_data/test-mobile-mechanics.txt
        loader = S3FileLoader(bucket="ragagentbucket", 
                              key="agent_data/test-mobile-mechanics.txt", 
                              aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
                              aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), 
                              region_name=os.getenv("AWS_DEFAULT_REGION"))

        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        all_splits = text_splitter.split_documents(docs)

        vector_store = FAISS.from_documents(all_splits, embeddings)
        vector_store.save_local("faiss_vector_store")
        print("Saved FAISS index to local storage")

    return vector_store
