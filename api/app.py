# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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

# Import RAG functionality
from rag_functionality import (
    rag_manager, 
    load_pdf_for_rag, 
    get_pdf_status, 
    generate_streaming_rag_response,
    generate_rag_response,
    is_pdf_loaded
)

# Initialize FastAPI application with a title
app = FastAPI(title="OpenAI Chat API")

# RAG functionality is now handled by rag_manager in rag_functionality.py

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

# Define the main chat endpoint that handles POST requests with RAG
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Check if PDF is loaded for RAG functionality
        if not is_pdf_loaded():
            raise HTTPException(status_code=400, detail="No PDF uploaded. Please upload a PDF first to use RAG functionality.")
        
        # Create an async generator function for streaming RAG responses
        async def generate():
            try:
                # Use RAG functionality to generate response
                async for chunk in generate_streaming_rag_response(
                    user_message=request.user_message,
                    api_key=request.api_key,
                    model=request.model
                ):
                    yield (chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8"))
            except Exception as e:
                print(f"Error in RAG generation: {str(e)}")
                yield f"Error: {str(e)}"

        # Return a streaming response to the client
        return StreamingResponse(generate(), media_type="text/plain")
    
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))

# Define PDF upload endpoint
@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), api_key: str = Form("")):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate API key
        if not api_key or not api_key.strip():
            raise HTTPException(status_code=400, detail="OpenAI API key is required")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Use RAG functionality to load PDF
            result = await load_pdf_for_rag(tmp_path, api_key)
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# Define PDF chat endpoint
@app.post("/api/pdf-chat")
async def pdf_chat(request: PDFChatRequest, stream: bool = False):
    if not is_pdf_loaded():
        raise HTTPException(status_code=400, detail="No PDF uploaded. Please upload a PDF first.")

    if stream:
        async def generate():
            async for chunk in generate_streaming_rag_response(
                user_message=request.user_message,
                api_key=request.api_key,
                model=request.model
            ):
                yield chunk if isinstance(chunk, bytes) else chunk.encode("utf-8")
        return StreamingResponse(generate(), media_type="text/plain")
    else:
        response_text = await generate_rag_response(
            user_message=request.user_message,
            api_key=request.api_key,
            model=request.model
        )
        return {"answer": response_text}


# Define endpoint to get current PDF status
@app.get("/api/pdf-status")
async def pdf_status():
    return get_pdf_status()

# Define a health check endpoint to verify API status
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
