import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
# openai.api_key = os.getenv("OPENAI_API_KEY") # Removed in new OpenAI library

class Chatbot:
    def __init__(self):
        self.client = OpenAI() # Initialize the OpenAI client
        self.conversation_history = []
        self.user_preferences = {}
        self.memory = []
        
    def add_to_memory(self, role, content):
        """Add a message to the conversation memory."""
        self.memory.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_conversation_context(self):
        """Get the recent conversation context."""
        # Keep last 5 messages for context
        recent_messages = self.memory[-5:] if len(self.memory) > 5 else self.memory
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
    
    def update_preferences(self, preferences):
        """Update user preferences."""
        self.user_preferences.update(preferences)
    
    def get_preferences_context(self):
        """Get user preferences as context."""
        if not self.user_preferences:
            return "No specific preferences set."
        return "\n".join([f"{key}: {value}" for key, value in self.user_preferences.items()])
    
    def generate_response(self, user_input):
        """Generate a response using OpenAI API with memory and context."""
        try:
            # Add user input to memory
            self.add_to_memory("User", user_input)
            
            # Prepare the conversation context
            conversation_context = self.get_conversation_context()
            preferences_context = self.get_preferences_context()
            
            # Create the system message with context
            system_message = f"""You are a helpful AI assistant with memory. 
            You remember previous conversations and user preferences.
            
            Recent conversation history:
            {conversation_context}
            
            User preferences:
            {preferences_context}
            
            Provide a helpful and contextual response based on the conversation history and user preferences."""
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            
            # Extract and store the response
            assistant_response = response.choices[0].message.content
            self.add_to_memory("Assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

def main():
    print("🤖 Welcome to the Memory-Enabled Chatbot!")
    print("Type 'quit' to exit, 'preferences' to set preferences, or 'history' to see conversation history.")
    print("-" * 50)
    
    chatbot = Chatbot()
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nThank you for chatting! Goodbye!")
            break
            
        elif user_input.lower() == 'preferences':
            print("\nSetting preferences (format: key=value, one per line)")
            print("Type 'done' when finished")
            while True:
                pref = input("Preference: ").strip()
                if pref.lower() == 'done':
                    break
                try:
                    key, value = pref.split('=')
                    chatbot.update_preferences({key.strip(): value.strip()})
                except:
                    print("Invalid format. Use key=value")
            print("Preferences updated!")
            
        elif user_input.lower() == 'history':
            print("\nConversation History:")
            for msg in chatbot.memory:
                print(f"[{msg['timestamp']}] {msg['role']}: {msg['content']}")
                
        else:
            response = chatbot.generate_response(user_input)
            print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main() 