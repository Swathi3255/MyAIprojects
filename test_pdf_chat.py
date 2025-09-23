#!/usr/bin/env python3
"""
Test script for the PDF Chat application.
This script tests the backend API endpoints.
"""

import requests
import os
import tempfile
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_PDF_PATH = None  # Set this to a test PDF file path

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_pdf_status():
    """Test the PDF status endpoint."""
    print("Testing PDF status...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/pdf-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PDF status: {data}")
            return True
        else:
            print(f"❌ PDF status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PDF status error: {e}")
        return False

def create_test_pdf():
    """Create a simple test PDF file."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a temporary PDF file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Create PDF content
        c = canvas.Canvas(temp_path, pagesize=letter)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 700, "This is a test document for the PDF chat application.")
        c.drawString(100, 650, "It contains sample text that can be used for testing.")
        c.drawString(100, 600, "The application should be able to extract this text")
        c.drawString(100, 550, "and answer questions about it.")
        c.save()
        
        return temp_path
    except ImportError:
        print("⚠️  reportlab not available, skipping PDF creation test")
        return None
    except Exception as e:
        print(f"❌ Error creating test PDF: {e}")
        return None

def test_pdf_upload(pdf_path, api_key=""):
    """Test PDF upload endpoint."""
    print("Testing PDF upload...")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            data = {'api_key': api_key}
            response = requests.post(f"{API_BASE_URL}/api/upload-pdf", files=files, data=data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PDF upload successful: {data}")
            return True
        else:
            print(f"❌ PDF upload failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ PDF upload error: {e}")
        return False

def test_pdf_chat(message, api_key=""):
    """Test PDF chat endpoint."""
    print(f"Testing PDF chat with message: '{message}'")
    try:
        data = {
            'user_message': message,
            'api_key': api_key,
            'model': 'gpt-4o-mini'
        }
        response = requests.post(f"{API_BASE_URL}/api/pdf-chat", json=data, stream=True)
        
        if response.status_code == 200:
            print("✅ PDF chat response:")
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    print(chunk, end='')
            print("\n")
            return True
        else:
            print(f"❌ PDF chat failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ PDF chat error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting PDF Chat API Tests")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Backend server is not running. Please start it first.")
        return
    
    # Test 2: PDF status (should be empty initially)
    test_pdf_status()
    
    # Test 3: Create test PDF
    test_pdf_path = create_test_pdf()
    if not test_pdf_path:
        print("❌ Cannot create test PDF. Please provide a test PDF file.")
        return
    
    try:
        # Test 4: Upload PDF
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            print("⚠️  OPENAI_API_KEY not set. Upload will fail without API key.")
        
        if test_pdf_upload(test_pdf_path, api_key):
            # Test 5: Check PDF status after upload
            test_pdf_status()
            
            # Test 6: Chat with PDF
            if api_key:
                test_pdf_chat("What is this document about?", api_key)
                test_pdf_chat("Summarize the main points.", api_key)
            else:
                print("⚠️  Skipping chat tests - no API key provided")
        
    finally:
        # Clean up test PDF
        if test_pdf_path and os.path.exists(test_pdf_path):
            os.unlink(test_pdf_path)
            print("🧹 Cleaned up test PDF file")
    
    print("=" * 50)
    print("✅ Tests completed!")

if __name__ == "__main__":
    main()
