import os
from dotenv import load_dotenv
from openai import OpenAI
import ast

# Load environment variables
load_dotenv()

# ====================
# ✅ Configuration
# ====================

# Initialize OpenAI
# openai.api_key = os.getenv("OPENAI_API_KEY") # Removed in new OpenAI library

# ====================
# ✅ Helper Functions
# ====================

def is_valid_python_code(code):
    """Check if the content is valid Python code."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def get_code_explanation(code):
    """Get code explanation using OpenAI API directly."""
    try:
        client = OpenAI() # Initialize the OpenAI client here
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an expert Python developer. Your task is to explain Python code in detail.
                Break down the code into sections and explain:
                1. What the code does overall
                2. Key functions and their purposes
                3. Important variables and their roles
                4. Any notable patterns or techniques used
                5. Potential improvements or best practices.
                
                Provide clear, concise, and educational explanations."""},
                {"role": "user", "content": f"Here's the code to explain:\n\n{code}"}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error getting code explanation: {str(e)}")

def read_python_file(file_path):
    """Read and return the contents of a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if not is_valid_python_code(content):
                print("\nError: The file does not contain valid Python code.")
                return None
            return content
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

# ====================
# ✅ Main Interaction Loop
# ====================

def main():
    print("🤖 Welcome to the Python Code Explainer!")
    print("This tool will explain any Python code file you provide.")
    print("Type 'quit' to exit the program.")
    print("-" * 50)
    
    while True:
        file_path = input("\nEnter the path to your Python file (or 'quit' to exit): ")
        if file_path.lower() == "quit":
            print("\nThank you for using the Python Code Explainer. Goodbye!")
            break
        
        # Check if file exists and is a Python file
        if not os.path.exists(file_path):
            print(f"\nError: File '{file_path}' does not exist.")
            continue
        
        if not file_path.endswith('.py'):
            print("\nError: Please provide a Python (.py) file.")
            continue
        
        # Read the file
        code = read_python_file(file_path)
        if code is None:
            continue
        
        try:
            print("\nAnalyzing your code...")
            # Get explanation
            explanation = get_code_explanation(code)
            print("\nCode Explanation:")
            print("-" * 50)
            print(explanation)
            print("-" * 50)
        except Exception as e:
            print(f"\nError generating explanation: {str(e)}")
            print("Please try again with a different file.")

if __name__ == "__main__":
    main()
