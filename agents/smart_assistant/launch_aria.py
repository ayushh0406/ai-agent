"""
🚀 Quick Launcher for ARIA Smart Assistant
"""
import sys
import os
import logging
from pathlib import Path

# Configure logging with colors for better readability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# Add project root to sys.path dynamically
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def preflight_checks():
    """Run basic environment and dependency checks before launch."""
    logging.info("🔍 Running pre-flight checks...")

    # Check for .env file and GROQ_API_KEY
    env_path = project_root / ".env"
    if not env_path.exists():
        logging.warning("⚠️  Missing `.env` file at project root")
    else:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        if not os.getenv("GROQ_API_KEY"):
            logging.warning("⚠️  GROQ_API_KEY not found in .env")

    # Optional: check microphone availability
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        if not devices:
            logging.warning("⚠️  No audio devices detected")
    except ImportError:
        logging.warning("⚠️  sounddevice not installed (required for voice input)")

def main():
    print("\n🚀 Launching ARIA Smart Assistant...")
    print("=" * 60)

    preflight_checks()

    try:
        from smart_runner import SmartAssistant
        
        assistant = SmartAssistant()
        assistant.run()

    except KeyboardInterrupt:
        logging.info("\n👋 ARIA shutting down gracefully... Bye!")
    except ModuleNotFoundError as e:
        logging.error(f"❌ Missing module: {e.name}")
        logging.info("💡 Try installing requirements with: pip install -r requirements.txt")
    except Exception as e:
        logging.exception(f"❌ Unexpected error while launching ARIA: {e}")
        logging.info("\n💡 Troubleshooting checklist:")
        logging.info("   1. Run: pip install -r requirements.txt")
        logging.info("   2. Ensure `.env` file contains a valid GROQ_API_KEY")
        logging.info("   3. Connect a working microphone (if using voice input)")
        logging.info("   4. Check your internet connection")

if __name__ == "__main__":
    main()
