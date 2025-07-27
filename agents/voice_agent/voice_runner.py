"""
Voice-Controlled AI Agent (Jarvis-Type)
Main runner for voice command processing with pydantic-ai
"""
import os
import sys
import speech_recognition as sr
import pyttsx3
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from groq import Groq

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import agent tools
from agents.code_writer.tool import write_code_file, read_code_file
from agents.file_manager.tool import sort_files_by_type, clean_empty_directories
from agents.email_assistant.tool import generate_email, save_email_draft
from agents.journal_agent.tool import log_journal_entry, get_mood_summary, search_journal_entries

# Load environment variables
load_dotenv()

class VoiceAIAgent:
    def __init__(self):
        """Initialize the voice-controlled AI agent"""
        self.setup_api_client()
        self.setup_voice_recognition()
        self.setup_text_to_speech()
        self.setup_agent()
        
    def setup_api_client(self):
        """Setup Groq API client"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ GROQ_API_KEY not found in .env file!")
            print("Please add your Groq API key to .env file")
            sys.exit(1)
        
        self.groq_client = Groq(api_key=api_key)
        
    def setup_voice_recognition(self):
        """Setup speech recognition"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("🎤 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("✅ Microphone calibrated!")
        
    def setup_text_to_speech(self):
        """Setup text-to-speech engine"""
        self.tts_enabled = os.getenv('TTS_ENABLED', 'true').lower() == 'true'
        
        if self.tts_enabled:
            self.tts_engine = pyttsx3.init()
            # Set voice properties
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)  # Use first available voice
            self.tts_engine.setProperty('rate', 180)  # Speech rate
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
        
    def setup_agent(self):
        """Setup pydantic-ai agent with tools"""
        # Create agent with all available tools
        self.agent = Agent(
            model="groq:mixtral-8x7b-32768",
            system_prompt="""You are Jarvis, a helpful voice-controlled AI assistant. 
            You can help with:
            - Writing and managing code files
            - Organizing files and directories  
            - Generating professional emails
            - Managing journal entries and mood tracking
            
            Always be concise but helpful in your responses. When users ask you to create files,
            use the appropriate tools to actually create them. Be friendly and efficient.""",
            retries=2
        )
        
        # Register tools with the agent
        self.register_tools()
        
    def register_tools(self):
        """Register all available tools with the agent"""
        # Code writer tools
        @self.agent.tool
        def create_code_file(filename: str, content: str, language: str = "python") -> str:
            """Create a code file with the specified content"""
            return write_code_file(filename, content, language)
            
        @self.agent.tool  
        def read_file(file_path: str) -> str:
            """Read the content of a code file"""
            return read_code_file(file_path)
            
        # File management tools
        @self.agent.tool
        def organize_files(directory: str) -> str:
            """Organize files in a directory by type"""
            return sort_files_by_type(directory)
            
        @self.agent.tool
        def cleanup_directories(directory: str) -> str:
            """Remove empty directories"""
            return clean_empty_directories(directory)
            
        # Email tools
        @self.agent.tool
        def create_email(purpose: str, recipient: str = "Sir/Madam", sender: str = "User", info: str = "") -> str:
            """Generate a professional email"""
            return generate_email(purpose, recipient, sender, info)
            
        @self.agent.tool
        def save_email(content: str, filename: str = None) -> str:
            """Save email as draft"""
            return save_email_draft(content, filename)
            
        # Journal tools
        @self.agent.tool
        def add_journal_entry(text: str, mood: str = "neutral", tags: str = "") -> str:
            """Add a new journal entry"""
            return log_journal_entry(text, mood, tags)
            
        @self.agent.tool
        def mood_analysis(days: int = 7) -> str:
            """Get mood summary for recent days"""
            return get_mood_summary(days)
            
        @self.agent.tool
        def search_journal(keyword: str, days: int = 30) -> str:
            """Search journal entries for keywords"""
            return search_journal_entries(keyword, days)
    
    def listen_for_command(self) -> str:
        """Listen for voice command and convert to text"""
        try:
            print("\n🎤 Listening... (Say something or 'exit' to quit)")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            print("🔍 Processing speech...")
            
            # Use Google Speech Recognition
            command = self.recognizer.recognize_google(
                audio, 
                language=os.getenv('VOICE_LANGUAGE', 'en-US')
            )
            
            print(f"🗣️ You said: '{command}'")
            return command.lower()
            
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            error_msg = "Sorry, I couldn't understand that. Please try again."
            print(f"❓ {error_msg}")
            self.speak(error_msg)
            return "unknown"
        except sr.RequestError as e:
            error_msg = f"Speech service error: {str(e)}"
            print(f"❌ {error_msg}")
            return "error"
    
    def speak(self, text: str):
        """Convert text to speech"""
        if self.tts_enabled and hasattr(self, 'tts_engine'):
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"❌ TTS Error: {e}")
        
    def process_command(self, command: str) -> str:
        """Process voice command using the AI agent"""
        try:
            print("🤖 Processing with AI agent...")
            
            # Use Groq API directly for now since pydantic-ai integration might need adjustment
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are Jarvis, a helpful voice-controlled AI assistant. 
                        Analyze the user's voice command and provide a helpful response.
                        
                        For file creation requests, provide the actual code/content.
                        For file organization, give specific instructions.
                        For emails, provide the email content.
                        For journaling, acknowledge the entry.
                        
                        Be concise but helpful."""
                    },
                    {"role": "user", "content": command}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Check if we need to execute any tools based on the command
            self.execute_tools_if_needed(command, ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def execute_tools_if_needed(self, command: str, ai_response: str):
        """Execute appropriate tools based on command analysis"""
        command_lower = command.lower()
        
        # Code creation commands
        if any(keyword in command_lower for keyword in ['create file', 'write file', 'make file', 'code file']):
            if 'python' in command_lower and 'hello' in command_lower:
                result = write_code_file('hello', 'print("Hello World!")', 'python')
                print(f"\n📁 {result}")
                
        # File organization commands  
        elif any(keyword in command_lower for keyword in ['organize', 'sort files', 'clean']):
            if 'download' in command_lower:
                downloads_path = str(Path.home() / 'Downloads')
                result = sort_files_by_type(downloads_path)
                print(f"\n📁 {result}")
                
        # Email commands
        elif any(keyword in command_lower for keyword in ['email', 'write email', 'draft']):
            if 'internship' in command_lower:
                result = generate_email('internship', additional_info="I am interested in software development.")
                print(f"\n📧 {result}")
                
        # Journal commands
        elif any(keyword in command_lower for keyword in ['journal', 'log', 'mood']):
            # Extract mood and text from command
            mood = 'neutral'
            if 'anxious' in command_lower:
                mood = 'anxious'
            elif 'happy' in command_lower:
                mood = 'happy'
            elif 'sad' in command_lower:
                mood = 'sad'
                
            result = log_journal_entry(command, mood)
            print(f"\n📔 {result}")
    
    def run(self):
        """Main loop for voice agent"""
        print("🚀 Voice AI Agent (Jarvis) is starting...")
        print("=" * 50)
        
        # Welcome message
        welcome_msg = "Hello! I'm Jarvis, your voice-controlled AI assistant. How can I help you today?"
        print(f"🤖 {welcome_msg}")
        self.speak(welcome_msg)
        
        while True:
            try:
                # Listen for command
                command = self.listen_for_command()
                
                # Handle special cases
                if command == "timeout":
                    continue
                elif command in ["unknown", "error"]:
                    continue
                elif any(exit_word in command for exit_word in ['exit', 'quit', 'bye', 'goodbye']):
                    farewell_msg = "Goodbye! Have a great day!"
                    print(f"🤖 {farewell_msg}")
                    self.speak(farewell_msg)
                    break
                
                # Process the command
                response = self.process_command(command)
                
                # Output response
                print(f"\n🤖 Jarvis: {response}")
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n👋 Exiting voice agent...")
                break
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                print(f"❌ {error_msg}")
                self.speak("Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and add your API keys")
        print("\nExample:")
        print("cp .env.example .env")
        print("# Then edit .env file with your actual API keys")
        sys.exit(1)
    
    try:
        agent = VoiceAIAgent()
        agent.run()
    except Exception as e:
        print(f"❌ Failed to start voice agent: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your microphone is connected")
        print("2. Check your .env file has GROQ_API_KEY")
        print("3. Install required packages: pip install -r requirements.txt")
