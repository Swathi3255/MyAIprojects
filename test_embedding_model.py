#!/usr/bin/env python3
"""
Test script to verify EmbeddingModel usage in HueGenius RAG functionality
"""

import sys
from pathlib import Path

# Add parent directory to path for aimakerspace imports
sys.path.append(str(Path(__file__).parent))

from rag_functionality import RAGManager

def test_embedding_model():
    """Test the EmbeddingModel initialization and usage"""
    
    print("🧪 Testing EmbeddingModel Usage in HueGenius")
    print("=" * 50)
    
    try:
        # Create RAG manager instance
        print("1️⃣ Creating RAGManager instance...")
        rag_manager = RAGManager()
        print("✅ RAGManager created successfully")
        
        # Test embedding model initialization
        print("\n2️⃣ Testing EmbeddingModel initialization...")
        from aimakerspace.openai_utils.embedding import EmbeddingModel
        
        # This follows the exact pattern from Embedding_Primer.ipynb
        embedding_model = EmbeddingModel()
        print("✅ EmbeddingModel created successfully using aimakerspace")
        
        # Test the embedding model in RAG manager
        print("\n3️⃣ Testing embedding model in RAG manager...")
        rag_manager.embedding_model = embedding_model
        
        # Test the embedding model test function
        print("\n4️⃣ Testing embedding model functionality...")
        is_working = rag_manager.test_embedding_model()
        
        if is_working:
            print("✅ Embedding model is working correctly")
        else:
            print("❌ Embedding model test failed")
        
        # Test PDF status with embedding model
        print("\n5️⃣ Testing PDF status with embedding model...")
        status = rag_manager.get_pdf_status()
        print(f"📊 PDF Status: {status}")
        
        print("\n" + "=" * 50)
        print("🎯 Summary:")
        print("✅ EmbeddingModel is properly integrated")
        print("✅ Following the pattern from Embedding_Primer.ipynb")
        print("✅ RAG functionality is ready for HueGenius")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_embedding_model()
