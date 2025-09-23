#!/usr/bin/env python3
"""
Script to check OpenAI API usage and credits
"""
import os
import requests

def check_openai_usage():
    """Check OpenAI API usage and account status"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        print("💡 Set your API key: set OPENAI_API_KEY=your_key_here")
        return
    
    print("🔍 Checking OpenAI API Usage...")
    print("=" * 40)
    
    # Check usage
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Get usage information
        response = requests.get(
            'https://api.openai.com/v1/usage',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            usage_data = response.json()
            print("✅ API Usage Information:")
            print(f"   Total tokens used: {usage_data.get('total_usage', 'N/A')}")
            print(f"   Current period: {usage_data.get('period', 'N/A')}")
        else:
            print(f"❌ Usage check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking usage: {e}")
    
    # Test API key validity with a simple request
    print("\n🔑 Testing API Key Validity...")
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Simple test request
        test_data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Hello'}],
            'max_tokens': 5
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ API key is valid and working!")
            result = response.json()
            print(f"   Test response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ API key test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
            # Common error messages
            if response.status_code == 401:
                print("💡 This usually means your API key is invalid or expired")
            elif response.status_code == 429:
                print("💡 This usually means you've hit rate limits or run out of credits")
            elif response.status_code == 402:
                print("💡 This usually means you need to add payment method or have insufficient credits")
                
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Next Steps:")
    print("1. Visit https://platform.openai.com/usage to see detailed usage")
    print("2. Check your billing information in the OpenAI dashboard")
    print("3. Make sure you have a valid payment method on file")
    print("4. Verify your API key is correct and active")

if __name__ == "__main__":
    check_openai_usage()
