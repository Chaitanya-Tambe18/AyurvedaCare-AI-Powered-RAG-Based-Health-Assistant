import chromadb
from chromadb.config import Settings
import ollama
import numpy as np
from config import Config
import os
import warnings

# Disable all ChromaDB telemetry and warnings
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
os.environ['CHROMA_TELEMETRY'] = 'False'
warnings.filterwarnings("ignore", category=UserWarning, module='chromadb')

class VectorStore:
    def __init__(self):
        # Disable Chroma telemetry completely
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=False,
                is_persistent=True
            )
        )
        self.collection = self.client.get_or_create_collection(
            name="health_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents, metadatas=None, ids=None):
        # Check for existing IDs to prevent duplicates
        if ids:
            existing_ids = set()
            try:
                existing_data = self.collection.get(ids=ids)
                if existing_data['ids']:
                    existing_ids = set(existing_data['ids'])
            except:
                pass
            
            # Filter out existing documents
            filtered_docs = []
            filtered_metadatas = []
            filtered_ids = []
            
            for doc, metadata, doc_id in zip(documents, metadatas or [None]*len(documents), ids):
                if doc_id not in existing_ids:
                    filtered_docs.append(doc)
                    if metadata is not None:
                        filtered_metadatas.append(metadata)
                    filtered_ids.append(doc_id)
            
            if not filtered_docs:
                print("All documents already exist in vector store")
                return
            
            documents = filtered_docs
            metadatas = filtered_metadatas if filtered_metadatas else None
            ids = filtered_ids
        
        embeddings = []
        for doc in documents:
            try:
                response = ollama.embeddings(
                    model=Config.EMBEDDING_MODEL,
                    prompt=doc
                )
                embeddings.append(response['embedding'])
            except Exception as e:
                print(f"Error generating embedding for document: {str(e)}")
                continue
        
        if embeddings and documents:
            self.collection.add(
                documents=documents[:len(embeddings)],
                embeddings=embeddings,
                metadatas=metadatas[:len(embeddings)] if metadatas else None,
                ids=ids[:len(embeddings)] if ids else None
            )
            print(f"Added {len(embeddings)} new documents to vector store")
    
    def query(self, query_text, n_results=5):
        try:
            response = ollama.embeddings(
                model=Config.EMBEDDING_MODEL,
                prompt=query_text
            )
            query_embedding = response['embedding']
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return results
        except Exception as e:
            print(f"Error querying vector store: {str(e)}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def get_collection_count(self):
        try:
            return self.collection.count()
        except:
            return 0
    
    def clear_collection(self):
        try:
            self.client.delete_collection("health_documents")
            self.collection = self.client.get_or_create_collection(
                name="health_documents",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error clearing collection: {str(e)}")
