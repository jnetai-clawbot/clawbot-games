#!/usr/bin/env python3
"""
ClawBot AI Chat - Terminal Chat Interface
Chat with AI directly from your terminal
"""

import os
import sys
import json
import subprocess

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("MODEL", "llama3.2")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    print("""
╔═══════════════════════════════════════╗
║      🤖 ClawBot AI Chat              ║
║      Type 'exit' to quit              ║
║      Type 'clear' to clear screen     ║
╚═══════════════════════════════════════╝
    """)

def chat_with_ai(prompt):
    """Send prompt to local AI and get response"""
    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        result = subprocess.run(
            ['curl', '-s', '-X', 'POST', API_URL, 
             '-H', 'Content-Type: application/json',
             '-d', json.dumps(payload)],
            capture_output=True, text=True, timeout=120
        )
        
        response = json.loads(result.stdout)
        return response.get('response', 'No response')
        
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    clear_screen()
    print_banner()
    
    print("💬 Ready to chat! (Press Enter to send)\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                clear_screen()
                print_banner()
                continue
            
            print("\n🤖 ClawBot: ", end="", flush=True)
            response = chat_with_ai(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Bye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
