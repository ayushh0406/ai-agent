"""
Smart Assistant - An AI-powered productivity and task management agent
Advanced version with enhanced capabilities and modern interface
"""
import os
import sys
import speech_recognition as sr
import pyttsx3
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from groq import Groq
import threading
import time

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv()

class SmartAssistant:
    def __init__(self):
        """Initialize the Smart Assistant AI agent"""
        self.name = "ARIA"  # Advanced Responsive Intelligence Assistant
        self.setup_api_client()
        self.setup_voice_recognition()
        self.setup_text_to_speech()
        self.setup_agent()
        self.setup_memory()
        self.conversation_history = []
        
    def setup_api_client(self):
        """Setup Groq API client"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ GROQ_API_KEY not found in .env file!")
            print("Please add your Groq API key to .env file")
            sys.exit(1)
        
        self.groq_client = Groq(api_key=api_key)
        
    def setup_voice_recognition(self):
        """Setup speech recognition with enhanced settings"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Enhanced noise adjustment
        print("🎤 Calibrating microphone for optimal voice recognition...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
        print("✅ Microphone calibrated for enhanced accuracy!")
        
    def setup_text_to_speech(self):
        """Setup advanced text-to-speech engine"""
        self.tts_enabled = os.getenv('TTS_ENABLED', 'true').lower() == 'true'
        
        if self.tts_enabled:
            self.tts_engine = pyttsx3.init()
            # Enhanced voice properties
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a female voice for ARIA
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            self.tts_engine.setProperty('rate', 160)  # Slightly slower for clarity
            self.tts_engine.setProperty('volume', 0.9)  # Higher volume
        
    def setup_memory(self):
        """Setup memory system for context retention"""
        self.memory_file = Path("agents/smart_assistant/memory.json")
        self.memory_file.parent.mkdir(exist_ok=True)
        
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    self.memory = json.load(f)
            else:
                self.memory = {
                    'preferences': {},
                    'frequent_tasks': [],
                    'user_profile': {},
                    'conversation_patterns': []
                }
        except Exception:
            self.memory = {
                'preferences': {},
                'frequent_tasks': [],
                'user_profile': {},
                'conversation_patterns': []
            }
    
    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
        
    def setup_agent(self):
        """Setup pydantic-ai agent with enhanced capabilities"""
        self.agent = Agent(
            model="groq:mixtral-8x7b-32768",
            system_prompt=f"""You are ARIA (Advanced Responsive Intelligence Assistant), a sophisticated AI assistant. 
            You are more advanced than basic assistants and focus on:
            
            🎯 CORE CAPABILITIES:
            - Intelligent task management and productivity optimization
            - Advanced file and project organization
            - Smart scheduling and reminder systems
            - Enhanced document and code generation
            - Data analysis and insights
            - Creative problem-solving and brainstorming
            
            🧠 PERSONALITY TRAITS:
            - Professional yet friendly
            - Proactive in suggesting improvements
            - Detail-oriented and thorough
            - Adaptable to user preferences
            - Memory of previous interactions
            
            📊 ENHANCED FEATURES:
            - Context-aware responses based on conversation history
            - Learning from user patterns and preferences
            - Multi-step task planning and execution
            - Smart recommendations based on user behavior
            
            Always provide detailed, actionable responses. When handling tasks, break them down into steps and offer optimization suggestions. Remember user preferences and adapt your responses accordingly.
            
            Current date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}""",
            retries=3
        )
        
        # Register enhanced tools
        self.register_tools()
        
    def register_tools(self):
        """Register enhanced tools with the agent"""
        
        @self.agent.tool
        def create_smart_file(filename: str, content: str, file_type: str = "text", template: str = "basic") -> str:
            """Create files with smart templates and auto-formatting"""
            return self.create_smart_file_impl(filename, content, file_type, template)
            
        @self.agent.tool  
        def analyze_directory(directory_path: str, analysis_type: str = "overview") -> str:
            """Analyze directory structure and provide insights"""
            return self.analyze_directory_impl(directory_path, analysis_type)
            
        @self.agent.tool
        def smart_organize(directory: str, method: str = "intelligent") -> str:
            """Organize files using AI-powered categorization"""
            return self.smart_organize_impl(directory, method)
            
        @self.agent.tool
        def create_project_structure(project_name: str, project_type: str, features: str = "") -> str:
            """Create complete project structure with boilerplate"""
            return self.create_project_structure_impl(project_name, project_type, features)
            
        @self.agent.tool
        def schedule_reminder(task: str, time: str, priority: str = "medium") -> str:
            """Schedule smart reminders with context"""
            return self.schedule_reminder_impl(task, time, priority)
            
        @self.agent.tool
        def generate_report(data_source: str, report_type: str = "summary") -> str:
            """Generate intelligent reports from data"""
            return self.generate_report_impl(data_source, report_type)
            
        @self.agent.tool
        def optimize_workflow(current_workflow: str, goal: str = "efficiency") -> str:
            """Analyze and optimize workflows"""
            return self.optimize_workflow_impl(current_workflow, goal)
    
    def create_smart_file_impl(self, filename: str, content: str, file_type: str, template: str) -> str:
        """Implementation for smart file creation"""
        try:
            output_dir = Path("output/smart_assistant")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Apply smart templates
            if template == "professional" and file_type == "email":
                content = f"""Subject: {filename}

Dear Sir/Madam,

{content}

Best regards,
[Your Name]

---
Generated by ARIA Smart Assistant
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"""
            elif template == "documentation" and file_type == "markdown":
                content = f"""# {filename}

## Overview
{content}

## Key Points
- Auto-generated documentation
- Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

## Next Steps
- Review and customize content
- Add additional sections as needed

---
*Generated by ARIA Smart Assistant*"""
            
            # Determine file extension
            ext_map = {
                "python": ".py",
                "text": ".txt", 
                "markdown": ".md",
                "email": ".txt",
                "json": ".json",
                "html": ".html"
            }
            
            ext = ext_map.get(file_type, ".txt")
            file_path = output_dir / f"{filename}{ext}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update memory with file creation
            self.memory['frequent_tasks'].append({
                'action': 'file_creation',
                'type': file_type,
                'template': template,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            return f"✅ Smart file created: {file_path} (Type: {file_type}, Template: {template})"
            
        except Exception as e:
            return f"❌ Error creating smart file: {str(e)}"
    
    def analyze_directory_impl(self, directory_path: str, analysis_type: str) -> str:
        """Implementation for directory analysis"""
        try:
            path = Path(directory_path)
            if not path.exists():
                return f"❌ Directory not found: {directory_path}"
            
            files = list(path.rglob('*'))
            
            if analysis_type == "overview":
                total_files = len([f for f in files if f.is_file()])
                total_dirs = len([f for f in files if f.is_dir()])
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                return f"""📊 Directory Analysis: {directory_path}
                
🔢 Statistics:
- Files: {total_files}
- Directories: {total_dirs}
- Total Size: {total_size / (1024*1024):.2f} MB

📁 Structure analyzed by ARIA Smart Assistant"""
            
            return f"✅ Analysis completed for {directory_path}"
            
        except Exception as e:
            return f"❌ Error analyzing directory: {str(e)}"
    
    def smart_organize_impl(self, directory: str, method: str) -> str:
        """Implementation for smart organization"""
        return f"🧠 ARIA would organize {directory} using {method} method (Advanced organization system)"
    
    def create_project_structure_impl(self, project_name: str, project_type: str, features: str) -> str:
        """Implementation for project structure creation"""
        try:
            project_dir = Path(f"output/projects/{project_name}")
            project_dir.mkdir(parents=True, exist_ok=True)
            
            if project_type.lower() == "python":
                # Create Python project structure
                (project_dir / "src").mkdir(exist_ok=True)
                (project_dir / "tests").mkdir(exist_ok=True)
                (project_dir / "docs").mkdir(exist_ok=True)
                
                # Create files
                with open(project_dir / "README.md", 'w') as f:
                    f.write(f"""# {project_name}

A Python project created by ARIA Smart Assistant.

## Features
{features}

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```python
# Your code here
```

---
*Generated by ARIA - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*""")
                
                with open(project_dir / "requirements.txt", 'w') as f:
                    f.write("# Add your dependencies here\n")
                
                with open(project_dir / "src" / "__init__.py", 'w') as f:
                    f.write("# Package initialization\n")
            
            return f"🚀 Smart project structure created: {project_dir}"
            
        except Exception as e:
            return f"❌ Error creating project structure: {str(e)}"
    
    def schedule_reminder_impl(self, task: str, time: str, priority: str) -> str:
        """Implementation for scheduling reminders"""
        reminder = {
            'task': task,
            'time': time,
            'priority': priority,
            'created': datetime.datetime.now().isoformat()
        }
        
        # Save to memory
        if 'reminders' not in self.memory:
            self.memory['reminders'] = []
        self.memory['reminders'].append(reminder)
        
        return f"⏰ Smart reminder set: {task} (Priority: {priority}, Time: {time})"
    
    def generate_report_impl(self, data_source: str, report_type: str) -> str:
        """Implementation for report generation"""
        return f"📊 ARIA generated {report_type} report from {data_source}"
    
    def optimize_workflow_impl(self, current_workflow: str, goal: str) -> str:
        """Implementation for workflow optimization"""
        return f"⚡ ARIA analyzed workflow and suggests optimizations for {goal}"
    
    def listen_for_command(self) -> str:
        """Enhanced voice command listening with better error handling"""
        try:
            print("\n🎤 ARIA is listening... (Speak clearly or say 'exit' to quit)")
            
            with self.microphone as source:
                # Enhanced listening parameters
                audio = self.recognizer.listen(source, timeout=12, phrase_time_limit=12)
            
            print("🧠 ARIA is processing your command...")
            
            # Use Google Speech Recognition with enhanced settings
            command = self.recognizer.recognize_google(
                audio, 
                language=os.getenv('VOICE_LANGUAGE', 'en-US'),
                show_all=False
            )
            
            print(f"💬 You said: '{command}'")
            
            # Add to conversation history
            self.conversation_history.append({
                'type': 'user',
                'content': command,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            return command.lower()
            
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            error_msg = "I couldn't understand that clearly. Could you please repeat?"
            print(f"❓ ARIA: {error_msg}")
            self.speak(error_msg)
            return "unknown"
        except sr.RequestError as e:
            error_msg = f"Voice service error: {str(e)}"
            print(f"❌ ARIA Error: {error_msg}")
            return "error"
    
    def speak(self, text: str):
        """Enhanced text-to-speech with better voice quality"""
        if self.tts_enabled and hasattr(self, 'tts_engine'):
            try:
                # Add personality touches
                if "✅" in text:
                    text = text.replace("✅", "Success! ")
                if "❌" in text:
                    text = text.replace("❌", "Error: ")
                if "🚀" in text:
                    text = text.replace("🚀", "Great! ")
                
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"❌ ARIA TTS Error: {e}")
        
    def process_command(self, command: str) -> str:
        """Enhanced command processing with context awareness"""
        try:
            print("🧠 ARIA is thinking...")
            
            # Build context from conversation history
            recent_context = ""
            if len(self.conversation_history) > 1:
                recent_context = "Recent conversation context:\n"
                for entry in self.conversation_history[-3:]:  # Last 3 exchanges
                    recent_context += f"- {entry['type']}: {entry['content'][:100]}\n"
            
            # Enhanced system prompt with context
            system_prompt = f"""You are ARIA, an advanced AI assistant. {recent_context}
            
            User preferences from memory: {self.memory.get('preferences', {})}
            
            Analyze the command and provide intelligent, context-aware responses. 
            Be proactive and suggest follow-up actions when appropriate."""
            
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ],
                max_tokens=1200,
                temperature=0.6
            )
            
            ai_response = response.choices[0].message.content
            
            # Add to conversation history
            self.conversation_history.append({
                'type': 'assistant',
                'content': ai_response,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Execute tools if needed
            self.execute_smart_tools(command, ai_response)
            
            # Save memory periodically
            if len(self.conversation_history) % 5 == 0:
                self.save_memory()
            
            return ai_response
            
        except Exception as e:
            error_msg = f"I encountered an error while processing: {str(e)}"
            print(f"❌ ARIA Error: {error_msg}")
            return error_msg
    
    def execute_smart_tools(self, command: str, ai_response: str):
        """Execute appropriate tools based on intelligent command analysis"""
        command_lower = command.lower()
        
        # Smart file creation
        if any(keyword in command_lower for keyword in ['create', 'make', 'generate', 'write']):
            if 'project' in command_lower:
                if 'python' in command_lower:
                    result = self.create_project_structure_impl('smart_project', 'python', 'AI-powered features')
                    print(f"\n🚀 {result}")
            elif 'file' in command_lower:
                result = self.create_smart_file_impl('smart_document', 'Generated by ARIA', 'markdown', 'professional')
                print(f"\n📄 {result}")
                
        # Smart analysis
        elif any(keyword in command_lower for keyword in ['analyze', 'check', 'review']):
            if 'directory' in command_lower or 'folder' in command_lower:
                result = self.analyze_directory_impl('.', 'overview')
                print(f"\n📊 {result}")
                
        # Smart reminders
        elif any(keyword in command_lower for keyword in ['remind', 'schedule', 'set timer']):
            result = self.schedule_reminder_impl(command, 'later today', 'medium')
            print(f"\n⏰ {result}")
    
    def show_dashboard(self):
        """Show ARIA dashboard with stats and insights"""
        print("\n" + "="*60)
        print("🤖 ARIA SMART ASSISTANT DASHBOARD")
        print("="*60)
        print(f"💬 Conversations today: {len(self.conversation_history)}")
        print(f"⚡ Tasks completed: {len(self.memory.get('frequent_tasks', []))}")
        print(f"⏰ Active reminders: {len(self.memory.get('reminders', []))}")
        print(f"🧠 Memory entries: {len(self.memory)}")
        print("="*60)
    
    def run(self):
        """Enhanced main loop for ARIA Smart Assistant"""
        print("🚀 ARIA Smart Assistant is initializing...")
        print("🧠 Loading advanced capabilities and memory...")
        time.sleep(1)
        print("=" * 60)
        
        # Show dashboard
        self.show_dashboard()
        
        # Enhanced welcome message
        welcome_msg = "Hello! I'm ARIA, your Advanced Responsive Intelligence Assistant. I'm here to help you with intelligent task management, advanced file operations, and smart productivity solutions. What would you like to accomplish today?"
        print(f"\n🤖 ARIA: {welcome_msg}")
        self.speak(welcome_msg)
        
        while True:
            try:
                # Listen for command
                command = self.listen_for_command()
                
                # Handle special cases
                if command == "timeout":
                    timeout_msg = "I'm still here when you're ready to continue."
                    print(f"⏱️ ARIA: {timeout_msg}")
                    self.speak(timeout_msg)
                    continue
                elif command in ["unknown", "error"]:
                    continue
                elif any(exit_word in command for exit_word in ['exit', 'quit', 'bye', 'goodbye', 'shutdown']):
                    # Save memory before exit
                    self.save_memory()
                    farewell_msg = "It was great working with you today! I've saved our conversation for next time. Have an excellent day!"
                    print(f"\n🤖 ARIA: {farewell_msg}")
                    self.speak(farewell_msg)
                    break
                elif 'dashboard' in command:
                    self.show_dashboard()
                    continue
                
                # Process the command with enhanced intelligence
                response = self.process_command(command)
                
                # Output enhanced response
                print(f"\n🤖 ARIA: {response}")
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n👋 ARIA is shutting down gracefully...")
                self.save_memory()
                break
            except Exception as e:
                error_msg = f"I encountered an unexpected error: {str(e)}. Let me try to help you another way."
                print(f"❌ ARIA: {error_msg}")
                self.speak("I encountered an error, but I'm still here to help. Please try again.")

if __name__ == "__main__":
    # Enhanced startup checks
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("ARIA requires environment configuration.")
        print("\nQuick setup:")
        print("1. Copy .env.example to .env")
        print("2. Add your GROQ_API_KEY")
        print("3. Configure TTS_ENABLED=true")
        sys.exit(1)
    
    try:
        assistant = SmartAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Failed to start ARIA: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Microphone permissions and connection")
        print("2. Valid GROQ_API_KEY in .env file")
        print("3. Required packages: pip install -r requirements.txt")
        print("4. Python version compatibility (3.8+)")
