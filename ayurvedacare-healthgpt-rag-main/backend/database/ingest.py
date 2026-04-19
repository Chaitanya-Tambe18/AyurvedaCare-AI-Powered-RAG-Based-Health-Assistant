import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pdf_loader import PDFLoader
from vector_store import VectorStore
from config import Config

class DocumentIngestor:
    def __init__(self):
        self.vector_store = VectorStore()
        self.pdf_loader = PDFLoader()
    
    def ingest_all_pdfs(self):
        print("Starting directory-based PDF ingestion...")
        
        try:
            # Use the new directory loader method
            all_documents, all_metadatas, all_ids = self.pdf_loader.load_directory()
            
            if not all_documents:
                print("No documents to ingest.")
                return
            
            print(f"Processing {len(all_documents)} document chunks...")
            self.vector_store.add_documents(
                documents=all_documents,
                metadatas=all_metadatas,
                ids=all_ids
            )
            print("Ingestion completed!")
            print(f"Total documents in collection: {self.vector_store.get_collection_count()}")
            
        except Exception as e:
            print(f"Error during ingestion: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    ingestor = DocumentIngestor()
    ingestor.ingest_all_pdfs()
