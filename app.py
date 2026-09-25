# ZQXLO - App Runner
from core import ZQXLO

def main():
    print("="*40)
    print("  ZQXLO ⚡ - AI that connects to everything")
    print("  Built by ktix-studio | Phase 1")
    print("="*40)
    
    zqx = ZQXLO()
    
    # Test 1
    print("\n--- Test 1: Google Search ---")
    result = zqx.search_google("Best AI tools 2026")
    print(result)
    
    # Test 2
    print("\n--- Test 2: URL Reader ---")
    result2 = zqx.read_url("https://example.com")
    print(result2)
    
    print("\n✅ Phase 1 Complete! ZQXLO is alive!")

if __name__ == "__main__":
    main() 
