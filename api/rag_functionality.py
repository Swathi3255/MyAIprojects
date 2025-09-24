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
    """
    Manages RAG functionality for HueGenius color psychology app
    """

    def __init__(self):
        self.pdf_vector_db: Optional[VectorDatabase] = None
        self.pdf_text_chunks: List[str] = []
        self.current_pdf_filename: Optional[str] = None
        self.embedding_model: Optional[EmbeddingModel] = None
        self.chat_model: Optional[ChatOpenAI] = None

    def is_pdf_loaded(self) -> bool:
        return self.pdf_vector_db is not None and len(self.pdf_text_chunks) > 0

    def get_pdf_status(self) -> Dict[str, Any]:
        return {
            "has_pdf": self.current_pdf_filename is not None,
            "filename": self.current_pdf_filename,
            "chunks_count": len(self.pdf_text_chunks) if self.pdf_text_chunks else 0,
            "embedding_model_ready": self.embedding_model is not None,
            "vector_db_ready": self.pdf_vector_db is not None
        }

    def test_embedding_model(self) -> bool:
        try:
            if self.embedding_model is None:
                return False
            print("✅ Embedding model is ready and functional")
            return True
        except Exception as e:
            print(f"❌ Embedding model test failed: {str(e)}")
            return False

    async def load_pdf(self, file_path: str, api_key: str) -> Dict[str, Any]:
        try:
            if api_key and api_key.strip():
                os.environ["OPENAI_API_KEY"] = api_key.strip()
            else:
                raise ValueError("OpenAI API key is required")

            print(f"Loading PDF: {file_path}")
            pdf_loader = PDFLoader(file_path)
            pdf_documents = pdf_loader.load_documents()
            print(f"PDF loaded successfully: {len(pdf_documents)} pages")

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            self.pdf_text_chunks = text_splitter.split_texts(pdf_documents)
            print(f"Text split into {len(self.pdf_text_chunks)} chunks")

            print("Creating EmbeddingModel using aimakerspace...")
            self.embedding_model = EmbeddingModel()
            print("✅ EmbeddingModel created successfully")

            if not self.test_embedding_model():
                raise Exception("Embedding model test failed")

            print("Creating VectorDatabase with embedding model...")
            self.pdf_vector_db = VectorDatabase(self.embedding_model)
            print("✅ VectorDatabase created successfully")

            print(f"Starting embedding creation for {len(self.pdf_text_chunks)} chunks...")
            await self.pdf_vector_db.abuild_from_list(self.pdf_text_chunks)
            print("Embedding creation completed successfully!")

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
        return f"""You are HueGenius, a specialized Color Psychology and Cultural Meanings AI assistant...
Context from PDF:
{context}"""

    def create_general_system_prompt(self, context: str) -> str:
        return f"""You are a helpful AI assistant that answers questions based on the provided context from a PDF document.
Context from PDF:
{context}"""

    async def generate_rag_response(self, user_message: str, api_key: str, model: str = "gpt-4o-mini") -> str:
        if not self.is_pdf_loaded():
            raise ValueError("No PDF loaded. Please upload a PDF first.")

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            raise ValueError("OpenAI API key is required")

        relevant_chunks = self.pdf_vector_db.search_by_text(user_message, k=5, return_as_text=True)
        context = "\n\n".join(relevant_chunks)

        color_keywords = [
            'color', 'colour', 'hue', 'psychology', 'cultural', 'culture',
            'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink',
            'marketing', 'branding', 'design', 'therapy', 'healing',
            'emotion', 'feeling', 'mood', 'atmosphere', 'environment'
        ]
        is_color_query = any(keyword.lower() in user_message.lower() for keyword in color_keywords)

        if is_color_query:
            system_message = self.create_color_psychology_system_prompt(context)
        else:
            system_message = self.create_general_system_prompt(context)

        try:
            print("Creating ChatOpenAI model...")
            self.chat_model = ChatOpenAI(model_name=model)
            print("ChatOpenAI model created successfully")

            print("Generating full (non-streaming) RAG response...")
            response = self.chat_model.run(
                [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                text_only=True
            )
            print("RAG response generated successfully")
            return response

        except Exception as e:
            print(f"Error generating RAG response: {str(e)}")
            raise e

    async def generate_streaming_rag_response(self, user_message: str, api_key: str, model: str = "gpt-4o-mini"):
        """
        Stubbed streaming: just calls non-streaming for now.
        Later, replace with proper async streaming.
        """
        full_response = await self.generate_rag_response(user_message, api_key, model)
        yield full_response.encode("utf-8")


# Global RAG manager instance
rag_manager = RAGManager()

# Convenience functions
async def load_pdf_for_rag(file_path: str, api_key: str) -> Dict[str, Any]:
    return await rag_manager.load_pdf(file_path, api_key)

def get_pdf_status() -> Dict[str, Any]:
    return rag_manager.get_pdf_status()

async def generate_rag_response(user_message: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    return await rag_manager.generate_rag_response(user_message, api_key, model)

async def generate_streaming_rag_response(user_message: str, api_key: str, model: str = "gpt-4o-mini"):
    async for chunk in rag_manager.generate_streaming_rag_response(user_message, api_key, model):
        yield chunk

def is_pdf_loaded() -> bool:
    return rag_manager.is_pdf_loaded()
