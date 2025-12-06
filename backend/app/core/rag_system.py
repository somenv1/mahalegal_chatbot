import os
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader, JSONLoader
import json

from ..core.config import settings


class RAGSystem:
    """
    Retrieval-Augmented Generation system for Maharashtra Traffic Law queries.
    Uses ChromaDB for vector storage and LangChain for retrieval and generation.
    """
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vectorstore = None
        self.qa_chain = None
        self.fines_data = {}
        
    def initialize(self):
        """Initialize the RAG system by loading the vector store"""
        if os.path.exists(settings.CHROMA_PERSIST_DIRECTORY):
            self.vectorstore = Chroma(
                collection_name=settings.COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY
            )
            self._setup_qa_chain()
        
        # Load fines data for quick lookup
        self._load_fines_data()
    
    def _load_fines_data(self):
        """Load Maharashtra fines data into memory for quick verification"""
        fines_path = os.path.join(settings.DATA_DIR, "maharashtra_fines_2024.json")
        if os.path.exists(fines_path):
            with open(fines_path, 'r') as f:
                data = json.load(f)
                self.fines_data = {item['violation_code']: item for item in data.get('violations', [])}
    
    def _setup_qa_chain(self):
        """Setup the QA chain with custom prompt template"""
        template = """You are a legal advisor specializing in Maharashtra traffic laws and the Motor Vehicles Act 2019.
Use the following context to answer questions about traffic violations, fines, and legal rights in Maharashtra.

Important guidelines:
1. Provide accurate information based on Maharashtra state traffic rules
2. Cite specific sections of the Motor Vehicles Act when applicable
3. Include fine amounts as per 2024 rates
4. Mention relevant resources: mahatrafficechallan.gov.in, Mumbai Traffic Police (103), ACB helpline (1064)
5. If uncertain, advise consulting a legal professional
6. Be respectful and professional in tone

Context:
{context}

Question: {question}

Detailed Answer:"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": settings.TOP_K_RESULTS}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def query(self, question: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Query the RAG system with a question
        
        Args:
            question: User's question about Maharashtra traffic laws
            conversation_history: Optional previous conversation context
            
        Returns:
            Dictionary containing answer and source documents
        """
        if not self.qa_chain:
            return {
                "answer": "System not initialized. Please ensure documents are ingested first.",
                "sources": []
            }
        
        # Add conversation context if provided
        context_question = question
        if conversation_history and len(conversation_history) > 0:
            context = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in conversation_history[-3:]  # Last 3 messages for context
            ])
            context_question = f"Previous context:\n{context}\n\nCurrent question: {question}"
        
        result = self.qa_chain({"query": context_question})
        
        sources = []
        if "source_documents" in result:
            sources = [
                doc.metadata.get("source", "Unknown") 
                for doc in result["source_documents"]
            ]
        
        return {
            "answer": result["result"],
            "sources": list(set(sources))  # Remove duplicates
        }
    
    def verify_fine(self, violation_code: str) -> Dict[str, Any]:
        """
        Verify fine amount for a specific violation code
        
        Args:
            violation_code: Code of the traffic violation
            
        Returns:
            Dictionary with fine details
        """
        if violation_code in self.fines_data:
            return self.fines_data[violation_code]
        
        return {
            "error": "Violation code not found",
            "message": "Please verify the violation code or contact Mumbai Traffic Police at 103"
        }
    
    def search_violation_by_type(self, violation_type: str) -> List[Dict[str, Any]]:
        """
        Search for violations matching a type/description
        
        Args:
            violation_type: Description or type of violation
            
        Returns:
            List of matching violations
        """
        matches = []
        search_term = violation_type.lower()
        
        for code, details in self.fines_data.items():
            if search_term in details.get('violation_name', '').lower() or \
               search_term in details.get('description', '').lower():
                matches.append(details)
        
        return matches


# Global RAG system instance
rag_system = RAGSystem()
