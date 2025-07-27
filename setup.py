"""
Setup script for Voice AI Agent
Installs all required packages and sets up the environment
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print(f"   Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def install_pyaudio_windows():
    """Special handling for PyAudio on Windows"""
    print("🔄 Installing PyAudio for Windows...")
    
    # Try pip install first
    if run_command("pip install pyaudio", "Installing PyAudio via pip"):
        return True
    
    print("⚠️ pip install failed, trying alternative method...")
    
    # Try installing wheel
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    architecture = "win_amd64" if sys.maxsize > 2**32 else "win32"
    
    wheel_url = f"https://github.com/intxcc/pyaudio_portaudio/releases/download/v19.7.0/PyAudio-0.2.11-cp{python_version.replace('.', '')}-cp{python_version.replace('.', '')}-{architecture}.whl"
    
    if run_command(f"pip install {wheel_url}", "Installing PyAudio from wheel"):
        return True
    
    print("❌ PyAudio installation failed!")
    print("📋 Manual installation steps:")
    print("1. Download PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
    print("2. Install using: pip install <downloaded_wheel_file>")
    return False

def main():
    """Main setup function"""
    print("🚀 Voice AI Agent Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        print("   Please run this script from the project root directory")
        return False
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("🔄 Creating .env file from template...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ .env file created!")
            print("⚠️ Please edit .env file and add your actual API keys")
        else:
            print("❌ .env.example not found!")
            return False
    
    # Install standard packages
    print("\n📦 Installing Python packages...")
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        print("⚠️ pip upgrade failed, continuing anyway...")
    
    # Install packages one by one for better error handling
    packages = [
        ("python-dotenv", "Environment variable support"),
        ("groq", "Groq API client"),
        ("pydantic-ai", "Pydantic AI framework"),
        ("openai", "OpenAI client"),
        ("pyttsx3", "Text-to-speech"),
        ("speechrecognition", "Speech recognition")
    ]
    
    failed_packages = []
    
    for package, description in packages:
        if not run_command(f"pip install {package}", f"Installing {package} ({description})"):
            failed_packages.append(package)
    
    # Special handling for PyAudio on Windows
    if os.name == 'nt':  # Windows
        if not install_pyaudio_windows():
            failed_packages.append("pyaudio")
    else:
        if not run_command("pip install pyaudio", "Installing PyAudio"):
            failed_packages.append("pyaudio")
    
    # Create output directories
    print("\n📁 Creating output directories...")
    directories = ["output", "email_drafts", "journal_entries"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Setup summary
    print("\n" + "=" * 40)
    print("🎯 SETUP SUMMARY")
    print("=" * 40)
    
    if failed_packages:
        print(f"❌ Failed to install: {', '.join(failed_packages)}")
        print("\n🔧 Troubleshooting:")
        if "pyaudio" in failed_packages:
            print("• PyAudio: Try installing Microsoft Visual C++ Build Tools")
            print("• Alternative: Use conda instead of pip")
        print("• Try running with administrator privileges")
        print("• Update pip: python -m pip install --upgrade pip")
        return False
    else:
        print("✅ All packages installed successfully!")
    
    # Next steps
    print("\n🎯 NEXT STEPS:")
    print("1. Edit .env file and add your Groq API key")
    print("2. Get a free API key from: https://console.groq.com/")
    print("3. Run the voice agent: python agents/voice_agent/voice_runner.py")
    
    # API key reminder
    print("\n🔑 API KEY SETUP:")
    print("Add this to your .env file:")
    print("GROQ_API_KEY=your_actual_api_key_here")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Setup completed successfully!")
        print("Ready to run your Voice AI Agent!")
    else:
        print("\n💥 Setup failed!")
        print("Please check the errors above and try again.")
        sys.exit(1)
