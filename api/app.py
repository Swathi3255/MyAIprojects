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
async def upload_pdf(file: UploadFile = File(...), api_key: str = Form("")):
    global pdf_vector_db, pdf_text_chunks, current_pdf_filename
    
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Set API key for OpenAI BEFORE creating any aimakerspace objects
        if api_key and api_key.strip():
            os.environ["OPENAI_API_KEY"] = api_key.strip()
            print(f"API key set successfully: {api_key[:10]}...")  # Debug log
        else:
            raise HTTPException(status_code=400, detail="OpenAI API key is required")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Load PDF using aimakerspace
            try:
                pdf_loader = PDFLoader(tmp_path)
                pdf_documents = pdf_loader.load_documents()
                print(f"PDF loaded successfully: {len(pdf_documents)} pages")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to load PDF: {str(e)}")
            
            # Split text into chunks
            try:
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                pdf_text_chunks = text_splitter.split_texts(pdf_documents)
                print(f"Text split into {len(pdf_text_chunks)} chunks")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to split text: {str(e)}")
            
            # Create vector database (API key should be set in environment now)
            try:
                print("DEBUG: Creating EmbeddingModel...")
                embedding_model = EmbeddingModel()
                print("DEBUG: EmbeddingModel created successfully")
                
                print("DEBUG: Creating VectorDatabase...")
                pdf_vector_db = VectorDatabase(embedding_model)
                print("DEBUG: VectorDatabase created successfully")
            except Exception as e:
                print(f"DEBUG: Error creating embedding model or vector database: {str(e)}")
                print(f"DEBUG: Error type: {type(e)}")
                import traceback
                print(f"DEBUG: Full traceback: {traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=f"Failed to initialize embedding model: {str(e)}")
            
            # Build vector database from chunks
            try:
                print(f"DEBUG: Starting embedding creation for {len(pdf_text_chunks)} chunks...")
                print(f"DEBUG: First chunk preview: {pdf_text_chunks[0][:100]}...")
                
                print("DEBUG: Calling abuild_from_list...")
                await pdf_vector_db.abuild_from_list(pdf_text_chunks)
                print("DEBUG: Embedding creation completed successfully!")
                
                print(f"DEBUG: Vector database now has {len(pdf_vector_db.vectors)} vectors")
            except Exception as e:
                print(f"DEBUG: Error during embedding creation: {str(e)}")
                print(f"DEBUG: Error type: {type(e)}")
                import traceback
                print(f"DEBUG: Full traceback: {traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=f"Failed to create embeddings: {str(e)}")
            
            current_pdf_filename = file.filename
            
            return {
                "message": f"PDF '{file.filename}' uploaded and indexed successfully",
                "filename": file.filename,
                "chunks_count": len(pdf_text_chunks),
                "has_pdf": True,
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
        
        # Set API key for OpenAI BEFORE creating any aimakerspace objects
        if request.api_key:
            os.environ["OPENAI_API_KEY"] = request.api_key
        else:
            raise HTTPException(status_code=400, detail="OpenAI API key is required")
        
        # Search for relevant chunks
        relevant_chunks = pdf_vector_db.search_by_text(request.user_message, k=5, return_as_text=True)
        
        # Create context from relevant chunks
        context = "\n\n".join(relevant_chunks)
        
        # Create specialized system message for Color Psychology
        system_message = f"""You are HueGenius, a specialized Color Psychology and Cultural Meanings AI assistant. You have access to comprehensive information about color psychology, cultural symbolism, and the psychological effects of colors across different societies.

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
        
        # Initialize chat model
        try:
            print("DEBUG: Creating ChatOpenAI model...")
            chat_model = ChatOpenAI(model_name=request.model)
            print("DEBUG: ChatOpenAI model created successfully")
        except Exception as e:
            print(f"DEBUG: Error creating ChatOpenAI model: {str(e)}")
            print(f"DEBUG: Error type: {type(e)}")
            import traceback
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize chat model: {str(e)}")
        
        # Create async generator for streaming response
        async def generate():
            try:
                print("DEBUG: Starting chat streaming...")
                async for chunk in chat_model.astream([
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": request.user_message}
                ]):
                    yield chunk
                print("DEBUG: Chat streaming completed successfully")
            except Exception as e:
                print(f"DEBUG: Error during chat streaming: {str(e)}")
                print(f"DEBUG: Error type: {type(e)}")
                import traceback
                print(f"DEBUG: Full traceback: {traceback.format_exc()}")
                yield f"Error: {str(e)}"
        
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
