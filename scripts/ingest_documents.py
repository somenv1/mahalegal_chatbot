#!/usr/bin/env python3
"""
Document Ingestion Script for Maharashtra Traffic Law Advisor

This script processes and ingests documents into ChromaDB for RAG system.
It handles markdown files and JSON data from the data directory.
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path to import from backend
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document


def load_markdown_documents(data_dir: str) -> list[Document]:
    """Load all markdown documents from data directory"""
    documents = []
    data_path = Path(data_dir)
    
    for md_file in data_path.glob("*.md"):
        print(f"Loading {md_file.name}...")
        loader = TextLoader(str(md_file), encoding='utf-8')
        docs = loader.load()
        
        # Add metadata
        for doc in docs:
            doc.metadata["source"] = md_file.name
            doc.metadata["type"] = "markdown"
        
        documents.extend(docs)
    
    return documents


def load_json_documents(data_dir: str) -> list[Document]:
    """Load and convert JSON files to documents"""
    documents = []
    data_path = Path(data_dir)
    
    for json_file in data_path.glob("*.json"):
        print(f"Loading {json_file.name}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process fines data
        if "violations" in data:
            for violation in data["violations"]:
                content = f"""
Violation: {violation.get('violation_name', 'Unknown')}
Code: {violation.get('violation_code', 'N/A')}
Section: {violation.get('section', 'N/A')}
Fine Amount: ₹{violation.get('fine_amount', 0)}
Description: {violation.get('description', 'No description available')}
"""
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": json_file.name,
                        "type": "fine_data",
                        "violation_code": violation.get('violation_code', 'N/A')
                    }
                )
                documents.append(doc)
            
            # Add general information
            if "payment_portal" in data:
                content = f"Payment Portal: {data['payment_portal']}\n"
                
                if "helplines" in data:
                    content += "\nHelplines:\n"
                    for name, number in data["helplines"].items():
                        content += f"- {name.replace('_', ' ').title()}: {number}\n"
                
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": json_file.name,
                        "type": "general_info"
                    }
                )
                documents.append(doc)
    
    return documents


def ingest_documents(data_dir: str = "./data", persist_dir: str = "./chroma_db"):
    """Main function to ingest all documents into ChromaDB"""
    
    print("=" * 60)
    print("Maharashtra Traffic Law Advisor - Document Ingestion")
    print("=" * 60)
    
    # Load documents
    print("\n1. Loading documents...")
    markdown_docs = load_markdown_documents(data_dir)
    json_docs = load_json_documents(data_dir)
    all_documents = markdown_docs + json_docs
    
    print(f"   Loaded {len(markdown_docs)} markdown documents")
    print(f"   Loaded {len(json_docs)} JSON-based documents")
    print(f"   Total: {len(all_documents)} documents")
    
    # Split documents into chunks
    print("\n2. Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(all_documents)
    print(f"   Created {len(chunks)} chunks")
    
    # Initialize embeddings
    print("\n3. Initializing embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("   Embeddings model ready")
    
    # Create vector store
    print("\n4. Creating vector store...")
    if os.path.exists(persist_dir):
        print(f"   Warning: {persist_dir} already exists. It will be overwritten.")
        import shutil
        shutil.rmtree(persist_dir)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="maharashtra_traffic_laws"
    )
    
    print(f"   Vector store created at {persist_dir}")
    
    # Test the vector store
    print("\n5. Testing vector store...")
    test_query = "What is the fine for not wearing a helmet?"
    results = vectorstore.similarity_search(test_query, k=3)
    print(f"   Test query: '{test_query}'")
    print(f"   Found {len(results)} relevant documents")
    
    print("\n" + "=" * 60)
    print("Document ingestion completed successfully!")
    print("=" * 60)
    print(f"\nYou can now start the backend server.")
    print(f"The RAG system will use the vector store from: {persist_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ingest documents for Maharashtra Traffic Law Advisor"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="./data",
        help="Directory containing source documents (default: ./data)"
    )
    parser.add_argument(
        "--persist-dir",
        type=str,
        default="./backend/chroma_db",
        help="Directory to store ChromaDB (default: ./backend/chroma_db)"
    )
    
    args = parser.parse_args()
    
    # Check if data directory exists
    if not os.path.exists(args.data_dir):
        print(f"Error: Data directory '{args.data_dir}' not found!")
        sys.exit(1)
    
    # Run ingestion
    try:
        ingest_documents(args.data_dir, args.persist_dir)
    except Exception as e:
        print(f"\nError during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
