from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core import (
    StorageContext,
    SimpleDirectoryReader, 
    VectorStoreIndex
    )

# 1. Init the embedding model
ollama_embedding = OllamaEmbedding("llama3.2", base_url="http://localhost:11434")
Settings.embed_model = ollama_embedding
Settings.llm = Ollama("llama3.2")

# 2. Storrage Context
storage_context = StorageContext()

# 3. Load documents from a folder
documents = SimpleDirectoryReader("app/data").load_data()

# 4. Add document and Storage to VectorStore
index = VectorStoreIndex.from_documents(
    documents
)

query_engin = index.as_query_engine()

resp = query_engin.query("Summarize the main topic.")

print(resp)