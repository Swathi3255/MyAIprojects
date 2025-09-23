#!/usr/bin/env python3
"""
Debug script to diagnose PDF chat errors step by step
"""
import requests
import json
import os
import sys

def test_api_endpoints():
    """Test all API endpoints to identify the issue"""
    base_url = "http://localhost:8000"
    
    print("🔍 PDF Chat Error Diagnostic Tool")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing API Health...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("💡 Make sure to start the backend with: cd api && python app.py")
        return
    
    # Test 2: PDF Status
    print("\n2️⃣ Checking PDF Status...")
    try:
        response = requests.get(f"{base_url}/api/pdf-status")
        if response.status_code == 200:
            status = response.json()
            print(f"📄 PDF Status: {status}")
            if not status.get('has_pdf'):
                print("❌ No PDF uploaded! This is likely the cause of your error.")
                print("💡 Upload a PDF file first before trying to chat.")
                return
            else:
                print("✅ PDF is uploaded and ready")
        else:
            print(f"❌ PDF status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ PDF status error: {e}")
    
    # Test 3: Test chat with minimal data
    print("\n3️⃣ Testing PDF Chat Endpoint...")
    
    # Get API key from environment or prompt
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        print("💡 Set your API key: set OPENAI_API_KEY=your_key_here")
        return
    
    try:
        chat_data = {
            'user_message': 'Test message',
            'api_key': api_key,
            'model': 'gpt-4o-mini'
        }
        
        print("📤 Sending test chat request...")
        response = requests.post(f"{base_url}/api/pdf-chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            print("✅ Chat endpoint is working!")
            print("📝 Response preview:")
            # Read first few chunks
            for i, chunk in enumerate(response.iter_content(chunk_size=1024, decode_unicode=True)):
                if chunk and i < 2:
                    print(f"   {chunk[:100]}...")
                if i >= 2:
                    break
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Chat request timed out - this might be the issue!")
        print("💡 The OpenAI API might be slow or your API key might be invalid")
    except Exception as e:
        print(f"❌ Chat test error: {e}")
    
    # Test 4: Check frontend-backend communication
    print("\n4️⃣ Testing Frontend-Backend Communication...")
    try:
        # Test if frontend can reach backend
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Backend is accessible from frontend")
        else:
            print("❌ Backend not accessible")
    except Exception as e:
        print(f"❌ Frontend-backend communication error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Common Solutions:")
    print("1. Make sure you've uploaded a PDF file first")
    print("2. Verify your OpenAI API key is valid and has credits")
    print("3. Check browser console for JavaScript errors")
    print("4. Ensure both frontend (port 3000) and backend (port 8000) are running")

if __name__ == "__main__":
    test_api_endpoints()
