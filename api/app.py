# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# Import Pydantic for data validation and settings management
from pydantic import BaseModel
# Import OpenAI client for interacting with OpenAI's API
from openai import OpenAI
import os
import tempfile
import shutil
from typing import Optional
from pathlib import Path

# Import aimakerspace components for RAG
import sys
sys.path.append(str(Path(__file__).parent.parent))
from aimakerspace.text_utils import PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.embedding import EmbeddingModel
from aimakerspace.openai_utils.chatmodel import ChatOpenAI

# Initialize FastAPI application with a title
app = FastAPI(title="OpenAI Chat API")

# Global variables for PDF processing and RAG
pdf_vector_db: Optional[VectorDatabase] = None
pdf_text_chunks: list = []
current_pdf_filename: Optional[str] = None

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the API to be accessed from different domains/origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers in requests
)

# Define the data model for chat requests using Pydantic
# This ensures incoming request data is properly validated
class ChatRequest(BaseModel):
    developer_message: str  # Message from the developer/system
    user_message: str      # Message from the user
    model: Optional[str] = "gpt-4.1-mini"  # Optional model selection with default
    api_key: str          # OpenAI API key for authentication

# Define the data model for PDF chat requests
class PDFChatRequest(BaseModel):
    user_message: str      # Message from the user
    model: Optional[str] = "gpt-4o-mini"  # Optional model selection with default
    api_key: str          # OpenAI API key for authentication

# Define the main chat endpoint that handles POST requests
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Initialize OpenAI client with the provided API key
        client = OpenAI(api_key=request.api_key)
        
        # Create an async generator function for streaming responses
        async def generate():
            # Create a streaming chat completion request
            stream = client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "developer", "content": request.developer_message},
                    {"role": "user", "content": request.user_message}
                ],
                stream=True  # Enable streaming response
            )
            
            # Yield each chunk of the response as it becomes available
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        # Return a streaming response to the client
        return StreamingResponse(generate(), media_type="text/plain")
    
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))

# Define PDF upload endpoint
@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), api_key: str = ""):
    global pdf_vector_db, pdf_text_chunks, current_pdf_filename
    
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Set API key for OpenAI
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Load PDF using aimakerspace
            pdf_loader = PDFLoader(tmp_path)
            pdf_documents = pdf_loader.load_documents()
            
            # Split text into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            pdf_text_chunks = text_splitter.split_texts(pdf_documents)
            
            # Create vector database
            embedding_model = EmbeddingModel()
            pdf_vector_db = VectorDatabase(embedding_model)
            
            # Build vector database from chunks
            await pdf_vector_db.abuild_from_list(pdf_text_chunks)
            
            current_pdf_filename = file.filename
            
            return {
                "message": f"PDF '{file.filename}' uploaded and indexed successfully",
                "filename": file.filename,
                "chunks_count": len(pdf_text_chunks),
                "status": "success"
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# Define PDF chat endpoint
@app.post("/api/pdf-chat")
async def pdf_chat(request: PDFChatRequest):
    global pdf_vector_db, pdf_text_chunks
    
    try:
        # Check if PDF is loaded
        if pdf_vector_db is None:
            raise HTTPException(status_code=400, detail="No PDF uploaded. Please upload a PDF first.")
        
        # Set API key for OpenAI
        os.environ["OPENAI_API_KEY"] = request.api_key
        
        # Search for relevant chunks
        relevant_chunks = pdf_vector_db.search_by_text(request.user_message, k=5, return_as_text=True)
        
        # Create context from relevant chunks
        context = "\n\n".join(relevant_chunks)
        
        # Create system message with context
        system_message = f"""You are a helpful assistant that answers questions based ONLY on the provided context from a PDF document. 
        
Context from PDF:
{context}

Instructions:
- Only answer questions using information from the provided context above
- If the question cannot be answered from the context, say "I cannot answer this question based on the provided PDF content"
- Be precise and cite specific information from the context when possible
- Do not make up information or use knowledge outside of the provided context"""
        
        # Initialize chat model
        chat_model = ChatOpenAI(model_name=request.model)
        
        # Create async generator for streaming response
        async def generate():
            async for chunk in chat_model.astream([
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.user_message}
            ]):
                yield chunk
        
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define endpoint to get current PDF status
@app.get("/api/pdf-status")
async def pdf_status():
    global current_pdf_filename, pdf_text_chunks
    return {
        "has_pdf": current_pdf_filename is not None,
        "filename": current_pdf_filename,
        "chunks_count": len(pdf_text_chunks) if pdf_text_chunks else 0
    }

# Define a health check endpoint to verify API status
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
