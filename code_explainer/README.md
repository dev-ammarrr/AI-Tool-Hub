# Python Code Explainer

This tool uses LangChain and OpenAI's GPT-3.5 to explain Python code files in detail. It provides comprehensive explanations of code structure, functions, variables, and best practices.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the script:
```bash
python main.py
```

2. When prompted, enter the path to any Python file you want to explain.

3. The tool will provide a detailed explanation of the code, including:
   - Overall purpose
   - Key functions and their purposes
   - Important variables and their roles
   - Notable patterns or techniques
   - Potential improvements or best practices

4. Type 'quit' to exit the program.

## Example

```bash
Enter the path to your Python file (or 'quit' to exit): path/to/your/file.py

Analyzing your code...

Code Explanation:
--------------------------------------------------
[Detailed explanation of your code will appear here]
--------------------------------------------------
```

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection for API access 