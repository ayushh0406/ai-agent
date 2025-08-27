"""
Quick Launcher for ARIA Smart Assistant
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def main():
    print("🚀 Launching ARIA Smart Assistant...")
    print("=" * 50)
    
    try:
        from smart_runner import SmartAssistant
        
        assistant = SmartAssistant()
        assistant.run()
        
    except KeyboardInterrupt:
        print("\n👋 ARIA shutting down...")
    except Exception as e:
        print(f"❌ Error launching ARIA: {e}")
        print("\n💡 Make sure you have:")
        print("1. Installed requirements: pip install -r requirements.txt")
        print("2. Setup .env file with GROQ_API_KEY")
        print("3. Connected microphone for voice input")

if __name__ == "__main__":
    main()
