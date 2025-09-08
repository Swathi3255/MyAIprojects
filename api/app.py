# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# Import Pydantic for data validation and settings management
from pydantic import BaseModel
# Import OpenAI client for interacting with OpenAI's API
from openai import OpenAI
from openai import APIStatusError, AuthenticationError, RateLimitError, BadRequestError, APIConnectionError
import os
from typing import Optional

# Initialize FastAPI application with a title
app = FastAPI(title="OpenAI Chat API")

# Configure CORS (Cross-Origin Resource Sharing) middleware
# Derive allowed origins from environment. Supports comma-separated list.
# Defaults to local Vite dev server.
frontend_origins_env = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in frontend_origins_env.split(",") if origin.strip()]

# Optional origin regex (e.g., to allow Vercel preview deployments)
allowed_origin_regex = os.getenv("FRONTEND_ORIGIN_REGEX", None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for chat requests using Pydantic
# This ensures incoming request data is properly validated
class ChatRequest(BaseModel):
    developer_message: str  # Message from the developer/system
    user_message: str      # Message from the user
    model: Optional[str] = "gpt-4.1-mini"  # Optional model selection with default
    api_key: str          # OpenAI API key for authentication

# Define the main chat endpoint that handles POST requests
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Basic input validation
    if not request.api_key or not request.api_key.strip():
        raise HTTPException(status_code=400, detail="Missing OpenAI API key.")
    if not request.user_message or not request.user_message.strip():
        raise HTTPException(status_code=400, detail="Missing user_message.")
    if not request.developer_message or not request.developer_message.strip():
        raise HTTPException(status_code=400, detail="Missing developer_message.")

    try:
        # Initialize OpenAI client with the provided API key
        client = OpenAI(api_key=request.api_key.strip())

        # Create an async generator function for streaming responses
        async def generate():
            try:
                # Create a streaming chat completion request
                stream = client.chat.completions.create(
                    model=request.model,
                    messages=[
                        {"role": "developer", "content": request.developer_message},
                        {"role": "user", "content": request.user_message}
                    ],
                    stream=True
                )

                # Yield each chunk of the response as it becomes available
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
            except (AuthenticationError) as e:
                # Authentication issues (invalid API key)
                raise HTTPException(status_code=401, detail=str(e))
            except (RateLimitError) as e:
                # Rate limiting by the API
                raise HTTPException(status_code=429, detail=str(e))
            except (BadRequestError) as e:
                # Invalid request parameters (e.g., bad model)
                raise HTTPException(status_code=400, detail=str(e))
            except (APIConnectionError) as e:
                # Connectivity issues to OpenAI
                raise HTTPException(status_code=503, detail="Upstream connection error: " + str(e))
            except APIStatusError as e:
                # Non-2xx from OpenAI API
                raise HTTPException(status_code=e.status_code or 502, detail=str(e))

        # Return a streaming response to the client
        return StreamingResponse(generate(), media_type="text/plain")

    except HTTPException:
        # Re-raise mapped HTTP exceptions
        raise
    except Exception as e:
        # Handle any other errors that occur during processing
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Define a health check endpoint to verify API status
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
