# PDF Chat Application

This application allows you to upload PDF documents and chat with them using a RAG (Retrieval-Augmented Generation) system built with the `aimakerspace` library.

## Features

- **PDF Upload**: Upload PDF documents through a web interface
- **Text Extraction**: Automatically extract text from PDFs using PyPDF2
- **Vector Indexing**: Create embeddings and build a vector database for semantic search
- **RAG Chat**: Ask questions about your PDF content and get answers based only on the document
- **Streaming Responses**: Real-time streaming of AI responses
- **Context-Aware**: The AI only answers using information from your uploaded PDF

## Architecture

### Backend (FastAPI)
- **PDF Upload Endpoint**: `/api/upload-pdf` - Handles PDF file uploads and indexing
- **PDF Chat Endpoint**: `/api/pdf-chat` - Processes chat messages with PDF context
- **Status Endpoint**: `/api/pdf-status` - Returns current PDF status
- **Health Check**: `/api/health` - API health monitoring

### Frontend (React + Vite)
- **File Upload Interface**: Drag-and-drop PDF upload with validation
- **Chat Interface**: Real-time chat with streaming responses
- **Status Display**: Shows current PDF information and indexing status
- **API Key Management**: Secure API key input for OpenAI

### RAG System (aimakerspace)
- **PDFLoader**: Extracts text from PDF files
- **CharacterTextSplitter**: Splits text into manageable chunks
- **VectorDatabase**: Stores embeddings for semantic search
- **EmbeddingModel**: Generates embeddings using OpenAI's API
- **ChatOpenAI**: Handles chat completions with context

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key

### Backend Setup

1. Navigate to the API directory:
   ```bash
   cd MyAIprojects/api
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key (optional, can also be set in the frontend):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. Run the backend server:
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd MyAIprojects/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **Start the Application**:
   - Start both backend (`python app.py`) and frontend (`npm run dev`) servers
   - Open `http://localhost:3000` in your browser

2. **Enter API Key**:
   - Enter your OpenAI API key in the input field at the top

3. **Upload PDF**:
   - Click "Choose PDF File" and select a PDF document
   - Wait for the upload and indexing to complete
   - You'll see a confirmation message with the number of text chunks created

4. **Chat with PDF**:
   - Type questions about your PDF content in the chat input
   - The AI will answer based only on the information in your PDF
   - Responses stream in real-time

## API Endpoints

### POST `/api/upload-pdf`
Upload and index a PDF document.

**Parameters**:
- `file`: PDF file (multipart/form-data)
- `api_key`: OpenAI API key (optional)

**Response**:
```json
{
  "message": "PDF 'filename.pdf' uploaded and indexed successfully",
  "filename": "filename.pdf",
  "chunks_count": 25,
  "status": "success"
}
```

### POST `/api/pdf-chat`
Chat with the uploaded PDF content.

**Request Body**:
```json
{
  "user_message": "What is the main topic of this document?",
  "api_key": "your-openai-api-key",
  "model": "gpt-4o-mini"
}
```

**Response**: Streaming text response

### GET `/api/pdf-status`
Get current PDF status.

**Response**:
```json
{
  "has_pdf": true,
  "filename": "document.pdf",
  "chunks_count": 25
}
```

## Technical Details

### RAG Implementation
1. **Document Processing**: PDFs are loaded and text is extracted page by page
2. **Text Chunking**: Text is split into 1000-character chunks with 200-character overlap
3. **Embedding Generation**: Each chunk is converted to a vector using OpenAI's text-embedding-3-small model
4. **Vector Storage**: Embeddings are stored in an in-memory vector database
5. **Semantic Search**: User queries are embedded and matched against document chunks
6. **Context Retrieval**: Top 5 most relevant chunks are retrieved for each query
7. **Response Generation**: LLM generates responses using only the retrieved context

### Security Features
- API key validation
- File type validation (PDF only)
- Temporary file cleanup
- Error handling and user feedback

### Performance Considerations
- In-memory vector storage (resets on server restart)
- Streaming responses for better user experience
- Chunked text processing for large documents
- Async operations for better scalability

## Troubleshooting

### Common Issues

1. **"No PDF uploaded" Error**:
   - Make sure you've uploaded a PDF file first
   - Check that the upload completed successfully

2. **API Key Issues**:
   - Ensure your OpenAI API key is valid and has sufficient credits
   - Check that the API key is entered correctly

3. **PDF Processing Errors**:
   - Ensure the PDF is not password-protected
   - Check that the PDF contains extractable text (not just images)

4. **CORS Issues**:
   - Make sure both frontend and backend are running
   - Check that the frontend is proxying requests to the backend correctly

### Development Tips

- Use browser developer tools to monitor network requests
- Check backend logs for detailed error messages
- Test with small PDF files first to verify the setup
- Monitor API usage in your OpenAI dashboard

## Future Enhancements

- Persistent vector storage (database integration)
- Support for multiple PDFs
- Document metadata extraction
- Advanced chunking strategies
- User authentication and session management
- PDF preview functionality
- Export chat conversations
