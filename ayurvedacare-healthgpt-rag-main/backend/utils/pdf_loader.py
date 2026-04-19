import PyPDF2
import os
import glob
from typing import List, Dict, Tuple
from config import Config

class PDFLoader:
    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
    
    def load_directory(self, directory_path: str = None) -> Tuple[List[str], List[Dict], List[str]]:
        """Load all PDFs from a directory and return documents, metadata, and IDs"""
        if directory_path is None:
            directory_path = Config.PDF_DATA_PATH
            
        pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
            return [], [], []
        
        all_documents = []
        all_metadatas = []
        all_ids = []
        
        print(f"Found {len(pdf_files)} PDF files in directory")
        
        for pdf_file in pdf_files:
            try:
                print(f"Processing {os.path.basename(pdf_file)}...")
                documents = self.load_pdf(pdf_file)
                
                for i, doc in enumerate(documents):
                    all_documents.append(doc)
                    all_metadatas.append({
                        "source": os.path.basename(pdf_file),
                        "page": i + 1,
                        "type": "pdf"
                    })
                    all_ids.append(f"{os.path.basename(pdf_file)}_page_{i+1}")
            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")
                continue
        
        return all_documents, all_metadatas, all_ids
    
    def load_pdf(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text.strip():
                            text += page_text + "\n"
                    except Exception as e:
                        print(f"Error extracting text from page {page_num}: {str(e)}")
                        continue
                
                chunks = self.chunk_text(text)
                return chunks
                
        except Exception as e:
            print(f"Error loading PDF {file_path}: {str(e)}")
            return []
    
    def chunk_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            if end >= len(text):
                chunk = text[start:].strip()
                if chunk:
                    chunks.append(chunk)
                break
            
            chunk = text[start:end]
            
            # Try to break at sentence boundaries
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            last_space = chunk.rfind(' ')
            
            best_break = max(last_period, last_newline, last_space)
            
            if best_break > start + self.chunk_size // 2:
                chunk = text[start:start + best_break + 1]
                start = start + best_break + 1
            else:
                start = end - self.chunk_overlap
            
            chunk = chunk.strip()
            if chunk:
                chunks.append(chunk)
        
        return chunks
