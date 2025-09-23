#!/usr/bin/env python3
"""
Detailed debug script to test PDF chat functionality after successful upload
"""
import requests
import json
import os
import sys

def test_chat_functionality():
    """Test the PDF chat endpoint in detail"""
    base_url = "http://localhost:8000"
    
    print("🔍 Detailed PDF Chat Debug Tool")
    print("=" * 50)
    
    # Test 1: Verify PDF is still uploaded
    print("\n1️⃣ Checking PDF Status...")
    try:
        response = requests.get(f"{base_url}/api/pdf-status")
        if response.status_code == 200:
            status = response.json()
            print(f"📄 PDF Status: {status}")
            if not status.get('has_pdf'):
                print("❌ PDF was lost! Please upload again.")
                return
            else:
                print("✅ PDF is still uploaded and ready")
        else:
            print(f"❌ PDF status check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ PDF status error: {e}")
        return
    
    # Test 2: Get API key
    print("\n2️⃣ Checking API Key...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        print("💡 Set your API key: set OPENAI_API_KEY=your_key_here")
        print("💡 Or enter it in the frontend interface")
        return
    else:
        print(f"✅ API key found: {api_key[:10]}...")
    
    # Test 3: Test chat with detailed error handling
    print("\n3️⃣ Testing PDF Chat Endpoint...")
    
    chat_data = {
        'user_message': 'What is this document about?',
        'api_key': api_key,
        'model': 'gpt-4o-mini'
    }
    
    print("📤 Sending chat request...")
    print(f"   Request data: {json.dumps(chat_data, indent=2)}")
    
    try:
        # Test with a longer timeout
        response = requests.post(
            f"{base_url}/api/pdf-chat", 
            json=chat_data, 
            timeout=60,  # Longer timeout
            stream=True
        )
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📊 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Chat endpoint responded successfully!")
            print("📝 Reading response stream...")
            
            # Try to read the streaming response
            try:
                content_received = False
                for i, chunk in enumerate(response.iter_content(chunk_size=1024, decode_unicode=True)):
                    if chunk:
                        content_received = True
                        print(f"   Chunk {i+1}: {chunk[:100]}...")
                        if i >= 2:  # Limit output
                            print("   ... (truncated)")
                            break
                
                if not content_received:
                    print("❌ No content received in response stream")
                else:
                    print("✅ Response stream working correctly")
                    
            except Exception as e:
                print(f"❌ Error reading response stream: {e}")
                
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"   Error response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Chat request timed out after 60 seconds")
        print("💡 This suggests an issue with OpenAI API or your API key")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("💡 Check if the backend server is still running")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e)}")
    
    # Test 4: Test with different model
    print("\n4️⃣ Testing with different model...")
    try:
        chat_data_gpt4 = {
            'user_message': 'Hello',
            'api_key': api_key,
            'model': 'gpt-4'  # Try gpt-4 instead
        }
        
        response = requests.post(
            f"{base_url}/api/pdf-chat", 
            json=chat_data_gpt4, 
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ GPT-4 model works!")
        else:
            print(f"❌ GPT-4 also failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ GPT-4 test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Troubleshooting Steps:")
    print("1. Check your OpenAI API key is valid and has credits")
    print("2. Try a different model (gpt-4 instead of gpt-4o-mini)")
    print("3. Check browser console for JavaScript errors")
    print("4. Verify your OpenAI account has sufficient usage limits")
    print("5. Try restarting both frontend and backend servers")

if __name__ == "__main__":
    test_chat_functionality()
