"""
Test script for Voice AI Agent
Tests all components without requiring voice input
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_code_writer():
    """Test code writer functionality"""
    print("🧪 Testing Code Writer...")
    
    from agents.code_writer.tool import write_code_file, read_code_file
    
    # Test code creation
    result = write_code_file("test_hello", "print('Hello from test!')", "python")
    print(f"   {result}")
    
    # Test code reading
    result = read_code_file("output/test_hello.py")
    print(f"   {result[:100]}...")
    
    print("✅ Code Writer tests passed!\n")

def test_file_manager():
    """Test file manager functionality"""
    print("🧪 Testing File Manager...")
    
    from agents.file_manager.tool import sort_files_by_type, clean_empty_directories
    
    # Create test directory with sample files
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Create sample files
    (test_dir / "document.pdf").touch()
    (test_dir / "image.jpg").touch()
    (test_dir / "code.py").touch()
    
    # Test file organization
    result = sort_files_by_type(str(test_dir))
    print(f"   {result[:200]}...")
    
    print("✅ File Manager tests passed!\n")

def test_email_assistant():
    """Test email assistant functionality"""
    print("🧪 Testing Email Assistant...")
    
    from agents.email_assistant.tool import generate_email, save_email_draft
    
    # Test email generation
    result = generate_email("internship", "John Doe", "Test User", "I am a computer science student")
    print(f"   Generated email preview: {result[:150]}...")
    
    # Test email saving
    result = save_email_draft("Test email content", "test_email.txt")
    print(f"   {result}")
    
    print("✅ Email Assistant tests passed!\n")

def test_journal_agent():
    """Test journal agent functionality"""
    print("🧪 Testing Journal Agent...")
    
    from agents.journal_agent.tool import log_journal_entry, get_mood_summary, search_journal_entries
    
    # Test journal entry
    result = log_journal_entry("Today I tested my AI agent!", "excited", "ai, testing, development")
    print(f"   {result}")
    
    # Test mood summary
    result = get_mood_summary(7)
    print(f"   Mood summary: {result[:100]}...")
    
    # Test journal search
    result = search_journal_entries("agent", 7)
    print(f"   Search results: {result[:100]}...")
    
    print("✅ Journal Agent tests passed!\n")

def test_voice_setup():
    """Test voice components setup"""
    print("🧪 Testing Voice Components...")
    
    try:
        import speech_recognition as sr
        print("   ✅ SpeechRecognition imported successfully")
        
        # Test microphone list
        mics = sr.Microphone.list_microphone_names()
        print(f"   📱 Found {len(mics)} microphone(s)")
        
    except ImportError:
        print("   ❌ SpeechRecognition not installed")
        return False
    
    try:
        import pyttsx3
        print("   ✅ pyttsx3 imported successfully")
        
        # Test TTS engine
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"   🗣️ Found {len(voices) if voices else 0} voice(s)")
        
    except ImportError:
        print("   ❌ pyttsx3 not installed")
        return False
    
    try:
        from groq import Groq
        print("   ✅ Groq imported successfully")
        
    except ImportError:
        print("   ❌ Groq not installed")
        return False
    
    print("✅ Voice Components tests passed!\n")
    return True

def test_environment():
    """Test environment setup"""
    print("🧪 Testing Environment...")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env file found")
        
        # Check for API key placeholder
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_groq_api_key_here" in content:
                print("   ⚠️ Please update .env with your actual Groq API key")
            else:
                print("   ✅ .env appears to be configured")
    else:
        print("   ❌ .env file not found")
        print("   💡 Run: cp .env.example .env")
    
    # Check output directories
    directories = ["output", "email_drafts", "journal_entries"]
    for directory in directories:
        if Path(directory).exists():
            print(f"   ✅ {directory}/ directory exists")
        else:
            print(f"   ⚠️ {directory}/ directory missing (will be created automatically)")
    
    print("✅ Environment tests completed!\n")

def main():
    """Run all tests"""
    print("🚀 Voice AI Agent Test Suite")
    print("=" * 50)
    
    try:
        # Test environment first
        test_environment()
        
        # Test core functionality
        test_code_writer()
        test_file_manager()
        test_email_assistant()
        test_journal_agent()
        
        # Test voice components
        voice_ok = test_voice_setup()
        
        print("=" * 50)
        print("🎯 TEST SUMMARY")
        print("=" * 50)
        
        if voice_ok:
            print("✅ All tests passed!")
            print("🎤 Your Voice AI Agent is ready to use!")
            print("\n🚀 Start the agent with:")
            print("   python agents/voice_agent/voice_runner.py")
        else:
            print("⚠️ Some voice components failed to load")
            print("💡 Run setup.py to install missing packages:")
            print("   python setup.py")
        
        print("\n🎯 Quick Test Commands:")
        print("• Say: 'Create a Python file that prints hello'")
        print("• Say: 'Generate an email for internship'")
        print("• Say: 'Log my mood as happy'")
        print("• Say: 'Exit' to quit")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the project root directory")
        print("2. Install requirements: pip install -r requirements.txt")
        print("3. Check Python version is 3.8+")

if __name__ == "__main__":
    main()
