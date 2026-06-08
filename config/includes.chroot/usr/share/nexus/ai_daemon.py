import keyboard
import requests
import subprocess
import time
import logging

# Set up logging for the OS background processes
logging.basicConfig(filename='/var/log/nexus_ai.log', level=logging.INFO)

class NexusMind:
    def __init__(self):
        self.ai_endpoint = "http://127.0.0.1:11434/api/generate"
        self.model = "deepseek-r1:3b"
        logging.info("Nexus Mind Initialized. Waiting for triggers.")

    def trigger_ai_interface(self):
        """This function runs when you hit the global hotkey."""
        logging.info("Hotkey detected. Summoning AI UI overlay.")
        # In the full OS, this triggers the sliding/spreading animation for the chat window
        print("\n[NEXUS AGENT]: How can I assist your workflow today?")
        
    def ask_deepseek(self, prompt):
        """Communicates natively with the local DeepSeek model."""
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.ai_endpoint, json=payload)
            return response.json().get('response', 'Error parsing thought process.')
        except Exception as e:
            logging.error(f"AI Engine failure: {e}")
            return "System Error: Neural link offline."

def main_loop():
    mind = NexusMind()
    
    # Listen for Ctrl + Space anywhere in the OS to open the assistant
    keyboard.add_hotkey('ctrl+space', mind.trigger_ai_interface)
    
    print("⚡ Nexus Background AI Daemon is active. Press Ctrl+Space to summon.")
    
    # Keep the daemon running infinitely in the OS background
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main_loop()