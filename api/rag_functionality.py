#!/usr/bin/env python3
"""
RAG Functionality Module for HueGenius
Handles Retrieval-Augmented Generation for color psychology and cultural meanings
"""

import os
from typing import Optional, List, Dict, Any
from pathlib import Path
import sys

# Add parent directory to path for aimakerspace imports
sys.path.append(str(Path(__file__).parent.parent))

from aimakerspace.text_utils import PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.embedding import EmbeddingModel
from aimakerspace.openai_utils.chatmodel import ChatOpenAI

class RAGManager:
    """Manages RAG functionality for HueGenius color psychology app"""
    
    def __init__(self):
        self.pdf_vector_db: Optional[VectorDatabase] = None
        self.pdf_text_chunks: List[str] = []
        self.current_pdf_filename: Optional[str] = None
        self.embedding_model: Optional[EmbeddingModel] = None
        self.chat_model: Optional[ChatOpenAI] = None
        
    def is_pdf_loaded(self) -> bool:
        """Check if a PDF is currently loaded and processed"""
        return self.pdf_vector_db is not None and len(self.pdf_text_chunks) > 0
    
    def get_pdf_status(self) -> Dict[str, Any]:
        """Get current PDF status"""
        return {
            "has_pdf": self.current_pdf_filename is not None,
            "filename": self.current_pdf_filename,
            "chunks_count": len(self.pdf_text_chunks) if self.pdf_text_chunks else 0
        }
    
    async def load_pdf(self, file_path: str, api_key: str) -> Dict[str, Any]:
        """Load and process a PDF file for RAG"""
        try:
            # Set API key for OpenAI
            if api_key and api_key.strip():
                os.environ["OPENAI_API_KEY"] = api_key.strip()
            else:
                raise ValueError("OpenAI API key is required")
            
            # Load PDF using aimakerspace
            print(f"Loading PDF: {file_path}")
            pdf_loader = PDFLoader(file_path)
            pdf_documents = pdf_loader.load_documents()
            print(f"PDF loaded successfully: {len(pdf_documents)} pages")
            
            # Split text into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            self.pdf_text_chunks = text_splitter.split_texts(pdf_documents)
            print(f"Text split into {len(self.pdf_text_chunks)} chunks")
            
            # Create embedding model and vector database
            print("Creating EmbeddingModel...")
            self.embedding_model = EmbeddingModel()
            print("EmbeddingModel created successfully")
            
            print("Creating VectorDatabase...")
            self.pdf_vector_db = VectorDatabase(self.embedding_model)
            print("VectorDatabase created successfully")
            
            # Build vector database from chunks
            print(f"Starting embedding creation for {len(self.pdf_text_chunks)} chunks...")
            await self.pdf_vector_db.abuild_from_list(self.pdf_text_chunks)
            print("Embedding creation completed successfully!")
            
            # Update filename
            self.current_pdf_filename = Path(file_path).name
            
            return {
                "message": f"PDF '{self.current_pdf_filename}' uploaded and indexed successfully",
                "filename": self.current_pdf_filename,
                "chunks_count": len(self.pdf_text_chunks),
                "has_pdf": True,
                "status": "success"
            }
            
        except Exception as e:
            print(f"Error loading PDF: {str(e)}")
            raise e
    
    def create_color_psychology_system_prompt(self, context: str) -> str:
        """Create specialized system prompt for color psychology"""
        return f"""You are HueGenius, a specialized Color Psychology and Cultural Meanings AI assistant. You have access to comprehensive information about color psychology, cultural symbolism, and the psychological effects of colors across different societies.

Your expertise includes:
- Psychological effects of colors on human behavior and emotions
- Cultural meanings and symbolism of colors across different societies
- Color psychology in marketing, branding, and design
- Color therapy and healing applications
- Gender and age-related color preferences
- Color combinations and their psychological effects
- Digital design and color psychology
- Interior design and color psychology

Context from PDF:
{context}

When answering questions about colors:
1. Provide specific psychological effects and cultural meanings
2. Include practical applications in design, marketing, and therapy
3. Mention cultural differences and sensitivities
4. Suggest appropriate color choices for specific contexts
5. Explain the science behind color psychology when relevant
6. Consider both universal and culture-specific meanings

Always prioritize cultural sensitivity and provide accurate, evidence-based information about color psychology."""
    
    def create_general_system_prompt(self, context: str) -> str:
        """Create general system prompt for non-color psychology queries"""
        return f"""You are a helpful AI assistant that answers questions based on the provided context from a PDF document.

Context from PDF:
{context}

Instructions:
- Answer questions using information from the provided context above
- If the question cannot be answered from the context, say "I cannot answer this question based on the provided PDF content"
- Be precise and cite specific information from the context when possible
- Do not make up information or use knowledge outside of the provided context"""
    
    async def generate_rag_response(self, user_message: str, api_key: str, model: str = "gpt-4o-mini") -> str:
        """Generate RAG response using loaded PDF content"""
        if not self.is_pdf_loaded():
            raise ValueError("No PDF loaded. Please upload a PDF first.")
        
        # Set API key
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            raise ValueError("OpenAI API key is required")
        
        # Search for relevant chunks
        relevant_chunks = self.pdf_vector_db.search_by_text(user_message, k=5, return_as_text=True)
        
        # Create context from relevant chunks
        context = "\n\n".join(relevant_chunks)
        
        # Determine if this is a color psychology query
        color_keywords = [
            'color', 'colour', 'hue', 'psychology', 'cultural', 'culture',
            'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink',
            'marketing', 'branding', 'design', 'therapy', 'healing',
            'emotion', 'feeling', 'mood', 'atmosphere', 'environment'
        ]
        
        is_color_query = any(keyword.lower() in user_message.lower() for keyword in color_keywords)
        
        # Create appropriate system message
        if is_color_query:
            system_message = self.create_color_psychology_system_prompt(context)
        else:
            system_message = self.create_general_system_prompt(context)
        
        # Initialize chat model
        try:
            print("Creating ChatOpenAI model...")
            self.chat_model = ChatOpenAI(model_name=model)
            print("ChatOpenAI model created successfully")
        except Exception as e:
            print(f"Error creating ChatOpenAI model: {str(e)}")
            raise e
        
        # Generate response
        try:
            print("Generating RAG response...")
            response = ""
            async for chunk in self.chat_model.astream([
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]):
                response += chunk
            
            print("RAG response generated successfully")
            return response
            
        except Exception as e:
            print(f"Error generating RAG response: {str(e)}")
            raise e
    
    async def generate_streaming_rag_response(self, user_message: str, api_key: str, model: str = "gpt-4o-mini"):
        """Generate streaming RAG response using loaded PDF content"""
        if not self.is_pdf_loaded():
            raise ValueError("No PDF loaded. Please upload a PDF first.")
        
        # Set API key
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            raise ValueError("OpenAI API key is required")
        
        # Search for relevant chunks
        relevant_chunks = self.pdf_vector_db.search_by_text(user_message, k=5, return_as_text=True)
        
        # Create context from relevant chunks
        context = "\n\n".join(relevant_chunks)
        
        # Determine if this is a color psychology query
        color_keywords = [
            'color', 'colour', 'hue', 'psychology', 'cultural', 'culture',
            'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink',
            'marketing', 'branding', 'design', 'therapy', 'healing',
            'emotion', 'feeling', 'mood', 'atmosphere', 'environment'
        ]
        
        is_color_query = any(keyword.lower() in user_message.lower() for keyword in color_keywords)
        
        # Create appropriate system message
        if is_color_query:
            system_message = self.create_color_psychology_system_prompt(context)
        else:
            system_message = self.create_general_system_prompt(context)
        
        # Initialize chat model
        try:
            print("Creating ChatOpenAI model...")
            self.chat_model = ChatOpenAI(model_name=model)
            print("ChatOpenAI model created successfully")
        except Exception as e:
            print(f"Error creating ChatOpenAI model: {str(e)}")
            raise e
        
        # Generate streaming response
        try:
            print("Starting streaming RAG response...")
            async for chunk in self.chat_model.astream([
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]):
                yield chunk
            print("Streaming RAG response completed successfully")
            
        except Exception as e:
            print(f"Error during streaming RAG response: {str(e)}")
            yield f"Error: {str(e)}"

# Global RAG manager instance
rag_manager = RAGManager()

# Convenience functions for easy import
async def load_pdf_for_rag(file_path: str, api_key: str) -> Dict[str, Any]:
    """Load PDF for RAG functionality"""
    return await rag_manager.load_pdf(file_path, api_key)

def get_pdf_status() -> Dict[str, Any]:
    """Get current PDF status"""
    return rag_manager.get_pdf_status()

async def generate_rag_response(user_message: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    """Generate RAG response"""
    return await rag_manager.generate_rag_response(user_message, api_key, model)

async def generate_streaming_rag_response(user_message: str, api_key: str, model: str = "gpt-4o-mini"):
    """Generate streaming RAG response"""
    async for chunk in rag_manager.generate_streaming_rag_response(user_message, api_key, model):
        yield chunk

def is_pdf_loaded() -> bool:
    """Check if PDF is loaded"""
    return rag_manager.is_pdf_loaded()
