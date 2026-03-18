import os
import json
import asyncio
from core.llm_engine import call_llm, build_prompt
from core.agent import run_agentic_pipeline

async def test_super_intelligence():
    print("🚀 Testing Super Intelligence Core (Gemini 1.5 Pro)...")
    
    mock_schema = {
        "tables": {
            "sales": {
                "columns": [
                    {"name": "revenue", "type": "numeric"},
                    {"name": "product", "type": "string"},
                    {"name": "date", "type": "date"}
                ]
            }
        }
    }
    
    user_query = "What is my total revenue per product?"
    
    print(f"Query: {user_query}")
    
    # Test individual LLM call
    prompt = build_prompt(user_query, mock_schema, [], [])
    response = call_llm(prompt)
    
    if response:
        print("[OK] LLM Response Received.")
        print(f"Preview: {response[:200]}...")
    else:
        print("[X] LLM Response Failed.")

if __name__ == "__main__":
    asyncio.run(test_super_intelligence())
