#!/usr/bin/env python3
"""
Debug script to test OpenAI client initialization step by step
"""
import os
import traceback

def debug_openai_init():
    print("=== DEBUG: Testing OpenAI Client Initialization ===")
    
    # Step 1: Check environment variable
    print("Step 1: Checking OPENAI_API_KEY environment variable...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ API key found: {api_key[:10]}...")
    else:
        print("❌ No API key found in environment")
        return
    
    # Step 2: Test OpenAI import
    print("\nStep 2: Testing OpenAI import...")
    try:
        from openai import OpenAI, AsyncOpenAI
        print("✅ OpenAI import successful")
    except Exception as e:
        print(f"❌ OpenAI import failed: {e}")
        return
    
    # Step 3: Test OpenAI client initialization with custom httpx client
    print("\nStep 3: Testing OpenAI client initialization with custom httpx client...")
    try:
        import httpx
        http_client = httpx.Client()
        client = OpenAI(api_key=api_key, http_client=http_client)
        print("✅ OpenAI client created successfully with custom httpx client")
    except Exception as e:
        print(f"❌ OpenAI client creation failed: {e}")
        print(f"Error type: {type(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return
    
    # Step 4: Test AsyncOpenAI client initialization with custom httpx client
    print("\nStep 4: Testing AsyncOpenAI client initialization with custom httpx client...")
    try:
        import httpx
        async_http_client = httpx.AsyncClient()
        async_client = AsyncOpenAI(api_key=api_key, http_client=async_http_client)
        print("✅ AsyncOpenAI client created successfully with custom httpx client")
    except Exception as e:
        print(f"❌ AsyncOpenAI client creation failed: {e}")
        print(f"Error type: {type(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return
    
    # Step 5: Test embedding creation
    print("\nStep 5: Testing embedding creation...")
    try:
        response = client.embeddings.create(
            input="Hello world",
            model="text-embedding-3-small"
        )
        print(f"✅ Embedding created successfully: {len(response.data[0].embedding)} dimensions")
    except Exception as e:
        print(f"❌ Embedding creation failed: {e}")
        print(f"Error type: {type(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return
    
    print("\n🎉 All tests passed! OpenAI client is working correctly.")

if __name__ == "__main__":
    # Set a test API key
    os.environ["OPENAI_API_KEY"] = "sk-proj-test-key-replace-with-real-key"
    debug_openai_init()
