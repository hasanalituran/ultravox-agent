from langchain_aws.embeddings import BedrockEmbeddings
from vector_store import FaissVectorStore
import logging
from boto_client import get_boto_client
import json
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",
                               aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                               aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

vector_store = FaissVectorStore(embeddings).create_vector_store()

async def retrieve_from_vector_store(query: str):
    """Retrieve information related to a query."""

    logger.info("Agent retrieving information for query: %s", query)

    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    
    return json.dumps(serialized)