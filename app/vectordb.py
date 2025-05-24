# Step 1: Import necessary libraries
import chromadb  # Chroma DB is used for persistent vector storage
from watchdog.observers import Observer  # For watching filesystem events (e.g., file changes)
from watchdog.events import FileSystemEventHandler  # To define custom responses to file changes
from llama_index.readers.file import UnstructuredReader  # Reads and parses unstructured files (like PDFs, DOCX)

# Step 2: Import LlamaIndex components
from llama_index.vector_stores.chroma import ChromaVectorStore  # Interface to use Chroma with LlamaIndex
from llama_index.core import (
    StorageContext,  # Helps manage where and how data is stored
    VectorStoreIndex,  # Indexing documents using vector embeddings
    SimpleDirectoryReader,  # (Commented out later) Reads all files in a directory
)
from llama_index.embeddings.ollama import OllamaEmbedding  # Generates embeddings using Ollama
from llama_index.llms.ollama import Ollama  # Language model from Ollama
from llama_index.core.settings import Settings  # Used to configure global LlamaIndex settings

# TODO complete
# this is a test
# Step 3: Define a class that watches a directory or file for changes
class DataDirWatcher(FileSystemEventHandler):
    def __init__(self, callback):  # Accept a callback function to trigger on file change
        super().__init__()
        self.callback = callback

    def on_any_event(self, event):  # Called whenever any change happens
        # Ignore directory changes and temp file edits (like swap files)
        if not event.is_directory and not event.src_path.endswith(("~", ".swp")):
            print(f"[watcher] Detected change: {event.event_type} - {event.src_path}")
            self.callback()  # Run the callback (e.g., rebuild the index)


# Step 4: Define the main class to handle Chroma + LlamaIndex logic
class ChromaLlamaIndexer:

    # Step 4.1: Initialize the indexer
    def __init__(self, 
                llm_model="llama3.2",  # Set the model name to use with Ollama
                chroma_dir="./chroma_db",  # Directory to store Chroma DB
                collection_name="default"):  # Chroma collection name

        self.embedding_model = OllamaEmbedding(model_name=llm_model)  # Create embedding model
        self.model = Ollama(model=llm_model)  # Create the language model

        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)  # Connect to persistent Chroma DB
        self.collection_name = self.chroma_client.get_or_create_collection(
            name=collection_name  # Create/get Chroma collection
        )

        # Configure LlamaIndex to use Ollama models
        Settings.llm = self.model
        Settings.embed_model = self.embedding_model

        # Set up the vector store interface
        self.vector_store = ChromaVectorStore(chroma_collection=self.collection_name)

        # Create storage context for saving and retrieving index data
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

        # Initialize index and query engine to None
        self.index = None
        self.query_engine = None

    # Step 4.2: Build or rebuild the index from a data file
    def build_index(self, data_path):
        print(f"[indexer] Loading documents from {data_path}…")
        
        # Option A (commented out): load all files from a folder
        # docs = SimpleDirectoryReader(data_path).load_data()

        # Option B (active): load a single file using UnstructuredReader
        loader = UnstructuredReader()
        docs = loader.load_data(file=data_path)

        # Create a new vector index from the loaded documents
        self.index = VectorStoreIndex.from_documents(
            documents=docs, 
            storage_context=self.storage_context
        )

        # Create a query engine to allow natural language queries
        self.query_engine = self.index.as_query_engine()

        print(f"[indexer] Index built: {len(docs)} documents ingested.")

    # Step 4.3: Handle queries to the indexed data
    def query(self, prompt):
        if self.query_engine is None:
            raise RuntimeError("Index not built yet. Call build_index() first.")
        return self.query_engine.query(prompt)  # Ask the LLM a question based on the indexed docs


# Step 5: Main function to run the indexing + watch loop
def main():
    DATA_DIR = "app/data/docdoc.docx"  # Path to the document you want to monitor and index

    # Step 5.1: Create the indexer instance
    indexer = ChromaLlamaIndexer(collection_name="my_docs")

    # Step 5.2: Build the initial index
    indexer.build_index(data_path=DATA_DIR)

    # Step 5.3: Set up file watcher to rebuild index if the file changes
    event_handler = DataDirWatcher(
        lambda: indexer.build_index(data_path=DATA_DIR),  # Pass a callback function
    )
    observer = Observer()
    observer.schedule(event_handler=event_handler, path=DATA_DIR, recursive=True)  # Watch the file path
    observer.daemon = True
    observer.start()
    print("[watcher] Watching for changes in", DATA_DIR)

    # Step 5.4: Start an interactive loop for user queries
    try:
        while True:
            user_query = input("\n🔍 Your query> ").strip()
            if not user_query:
                continue
            resp = indexer.query(user_query)
            print("\n📄 Response:\n", resp, "\n")
    except KeyboardInterrupt:
        print("\n[shutdown] Stopping watcher and exiting.")
        observer.stop()  # Stop watching
    observer.join()


# Step 6: Entry point for script
if __name__ == "__main__":
    main()  # Run main if script is executed directly
