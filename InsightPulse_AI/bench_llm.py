import sys
import os
from pathlib import Path

# Add core to path
sys.path.append(str(Path(__file__).parent))

from core.llm_engine import call_llm

def bench():
    print("--- BENCHMARKING LLM PATHWAYS ---")
    test_prompt = "Say 'SUCCESS' if you can read this."
    result = call_llm(test_prompt)
    if result:
        print(f"\n[FINAL RESULT] LLM is ALIVE: {result}")
    else:
        print("\n[FINAL RESULT] LLM is DEAD (returned None)")

if __name__ == "__main__":
    bench()
