#!/usr/bin/env python3
"""
Test script to verify Titanic PDF upload functionality.
"""

import requests
import os
import time

def test_titanic_upload():
    """Test uploading a Titanic-themed PDF."""
    
    API_BASE_URL = "http://localhost:8000"
    
    print("🚢 Testing Titanic PDF Upload")
    print("=" * 40)
    
    # Wait a moment for servers to start
    print("⏳ Waiting for servers to start...")
    time.sleep(3)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to start the backend with: cd api && python app.py")
        return
    
    # Test 2: Check if we have any PDF files
    pdf_files = []
    for file in os.listdir('.'):
        if file.endswith('.pdf'):
            pdf_files.append(file)
    
    if pdf_files:
        print(f"📄 Found PDF files: {pdf_files}")
        
        # Test 3: Try to upload the first PDF
        pdf_file = pdf_files[0]
        print(f"📤 Testing upload of: {pdf_file}")
        
        try:
            with open(pdf_file, 'rb') as f:
                files = {'file': f}
                data = {'api_key': os.getenv('OPENAI_API_KEY', '')}
                response = requests.post(f"{API_BASE_URL}/api/upload-pdf", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Upload successful!")
                print(f"   📊 Chunks created: {result.get('chunks_count', 'Unknown')}")
                print(f"   📁 Filename: {result.get('filename', 'Unknown')}")
                
                # Test 4: Try a chat query
                print("\n💬 Testing chat functionality...")
                chat_data = {
                    'user_message': 'What is this document about?',
                    'api_key': os.getenv('OPENAI_API_KEY', ''),
                    'model': 'gpt-4o-mini'
                }
                
                chat_response = requests.post(f"{API_BASE_URL}/api/pdf-chat", json=chat_data, stream=True)
                if chat_response.status_code == 200:
                    print("✅ Chat endpoint working!")
                    print("📝 Response preview:")
                    for i, chunk in enumerate(chat_response.iter_content(chunk_size=1024, decode_unicode=True)):
                        if chunk and i < 3:  # Show first few chunks
                            print(f"   {chunk[:100]}...")
                        if i >= 3:
                            break
                else:
                    print(f"❌ Chat test failed: {chat_response.status_code}")
                    
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
    else:
        print("❌ No PDF files found in current directory")
        print("💡 Available files:")
        for file in os.listdir('.'):
            if file.endswith(('.txt', '.pdf')):
                print(f"   📄 {file}")
    
    print("\n" + "=" * 40)
    print("🎯 Next steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Enter your OpenAI API key")
    print("3. Upload a PDF file")
    print("4. Start chatting about Titanic content!")

if __name__ == "__main__":
    test_titanic_upload()
