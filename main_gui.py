import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys
sys.path.append('./Text_Summarization')
from chatbot.chatbot import Chatbot
import threading
from code_explainer.main import get_code_explanation, read_python_file
from summarizer import Summarizer

class AIToolsHub:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Toolkit")
        self.root.geometry("1000x700")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use a modern theme
        
        # Define a modern color palette
        self.primary_color = "#007BFF" # Blue
        self.secondary_color = "#FFFFFF" # White
        self.background_color = "#F0F0F0" # Light Gray
        self.text_color = "#333333" # Dark Gray
        self.accent_color = "#FFC107" # Amber
        self.success_color = "#28a745" # Green
        self.info_color = "#17a2b8" # Light Blue
        self.warning_color = "#ffc107" # Yellow
        self.danger_color = "#dc3545" # Red
        
        # General styles
        self.style.configure('TFrame', background=self.background_color)
        self.style.configure('TLabel', background=self.background_color, foreground=self.text_color, font=('Helvetica', 10))
        
        # Button styles
        self.style.configure("Custom.TButton",
                             font=('Helvetica', 12, 'bold'),
                             padding=10,
                             borderwidth=0, # Remove border
                             relief="flat") # Flat button
        self.style.map("Custom.TButton",
                       background=[('active', self.secondary_color)],
                       foreground=[('active', self.primary_color)])

        # Entry style
        self.style.configure('TEntry',
                             fieldbackground=self.secondary_color,
                             foreground=self.text_color,
                             font=('Helvetica', 12),
                             padding=5,
                             borderwidth=1,
                             relief="solid")

        # ScrolledText (Text widget) style - ttk doesn't directly style ScrolledText, but we can style the internal Text widget
        # We'll use tags for messages directly on the Text widget, and for general text areas, we'll set background/foreground

        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for different tools
        self.frames = {}
        
        # Home frame
        self.frames['home'] = ttk.Frame(self.main_container)
        self.frames['home'].pack(fill=tk.BOTH, expand=True)
        self.create_home_frame()
        
        # Chatbot frame
        self.frames['chatbot'] = ttk.Frame(self.main_container)
        self.frames['chatbot'].pack(fill=tk.BOTH, expand=True)
        self.create_chatbot_frame()
        
        # Code Explainer frame
        self.frames['code_explainer'] = ttk.Frame(self.main_container)
        self.frames['code_explainer'].pack(fill=tk.BOTH, expand=True)
        self.create_code_explainer_frame()

        # Text Summarization frame
        self.frames['text_summarization'] = ttk.Frame(self.main_container)
        self.frames['text_summarization'].pack(fill=tk.BOTH, expand=True)
        self.create_text_summarization_frame()
        
        # Show home frame initially
        self.show_frame('home')
    
    def create_home_frame(self):
        """Create the home page with tool selection buttons"""
        frame = self.frames['home']
        
        # Menu button (3 dots) in top-left
        menu_btn = ttk.Button(
            frame,
            text="⋮",
            style="Custom.TButton",
            command=self.show_menu
        )
        menu_btn.place(x=10, y=10)
        
        # Main Title
        title_label = ttk.Label(
            frame,
            text="AI Toolkit",
            font=('Helvetica', 36, 'bold'),
            foreground=self.primary_color
        )
        title_label.pack(pady=(50, 10))
        
        # Separator line
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=100, pady=10)
        
        # Project Description
        desc_label = ttk.Label(
            frame,
            text="Your comprehensive desktop application for AI-powered tools.",
            font=('Helvetica', 12),
            wraplength=600,
            justify='center',
            foreground=self.text_color
        )
        desc_label.pack(pady=(10, 30), padx=50)
        
        # Projects Section Title
        projects_title = ttk.Label(
            frame,
            text="Explore Our Tools",
            font=('Helvetica', 20, 'bold'),
            foreground=self.primary_color
        )
        projects_title.pack(pady=(10, 20))
        
        # Container for project cards
        projects_container = ttk.Frame(frame)
        projects_container.pack(pady=0)
        
        # Define tools with descriptions (for cards)
        self.tools = [
            ("Chatbot", "An intelligent conversational AI assistant.", 'chatbot'),
            ("Code Explainer", "Understand complex code with detailed explanations and insights.", 'code_explainer'),
            ("Text Summarization", "Get concise summaries of long texts while preserving key information.", 'text_summarization')
        ]
        
        # Style for the individual project cards
        self.style.configure('ProjectCard.TFrame',
                             background=self.secondary_color,
                             relief='solid',
                             borderwidth=1,
                             padding=20)

        # Create project cards
        for tool_name, tool_desc, frame_name in self.tools:
            card_frame = ttk.Frame(projects_container, style='ProjectCard.TFrame')
            card_frame.pack(pady=10, padx=50, fill=tk.X)
            
            # Card Title (tool name)
            card_title = ttk.Label(
                card_frame,
                text=tool_name,
                font=('Helvetica', 16, 'bold'),
                foreground=self.primary_color,
                background=self.secondary_color
            )
            card_title.pack(pady=(0, 5))
            
            # Card Description
            card_description = ttk.Label(
                card_frame,
                text=tool_desc,
                font=('Helvetica', 10),
                foreground=self.text_color,
                background=self.secondary_color,
                wraplength=400,
                justify='center'
            )
            card_description.pack(pady=(0, 10))
            
            # Card Button
            card_button = ttk.Button(
                card_frame,
                text="Launch " + tool_name,
                style="Custom.TButton",
                command=lambda f=frame_name: self.show_frame(f)
            )
            card_button.pack(pady=(5, 0), fill=tk.X)
    
    def create_chatbot_frame(self):
        """Create the chatbot interface"""
        frame = self.frames['chatbot']
        
        # Back button
        back_btn = ttk.Button(
            frame,
            text="← Back to Home",
            style="Custom.TButton",
            command=lambda: self.show_frame('home')
        )
        back_btn.pack(pady=10, padx=10, anchor='w')
        
        # Title
        title_label = ttk.Label(
            frame,
            text="AI Chatbot",
            font=('Helvetica', 20, 'bold')
        )
        title_label.pack(pady=10)
        
        # Initialize chatbot
        self.chatbot = Chatbot()
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=('Helvetica', 11),
            background=self.secondary_color,
            foreground=self.text_color
        )
        self.chat_display.pack(pady=15, padx=25, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for chat messages
        self.chat_display.tag_configure('user', foreground='#0056b3', font=('Helvetica', 11, 'bold'), justify='right')
        self.chat_display.tag_configure('assistant', foreground='#1e7e34', font=('Helvetica', 11))
        self.chat_display.tag_configure('system', foreground='#dc2835', font=('Helvetica', 11, 'italic')) # Darker Red for system messages
        
        # Input frame
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=25, pady=(0, 15))
        
        # Message input
        self.message_input = ttk.Entry(
            input_frame,
            font=('Helvetica', 12)
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_input.bind("<Return>", self.send_message)
        
        # Send button
        send_button = ttk.Button(
            input_frame,
            text="Send",
            style="Custom.TButton",
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT)
        
        # Welcome message
        self.add_message("Assistant", "Hello! How can I help you today?")
    
    def create_code_explainer_frame(self):
        """Create the code explainer interface"""
        frame = self.frames['code_explainer']
        
        # Back button
        back_btn = ttk.Button(
            frame,
            text="← Back to Home",
            style="Custom.TButton",
            command=lambda: self.show_frame('home')
        )
        back_btn.pack(pady=10, padx=10, anchor='w')
        
        # Title
        title_label = ttk.Label(
            frame,
            text="Code Explainer",
            font=('Helvetica', 20, 'bold')
        )
        title_label.pack(pady=10)
        
        # Code input area
        code_label = ttk.Label(frame, text="Enter your code:", font=('Helvetica', 12))
        code_label.pack(pady=5)
        
        self.code_input = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=('Courier', 11),
            background=self.secondary_color,
            foreground=self.text_color
        )
        self.code_input.pack(pady=10, padx=25, fill=tk.BOTH, expand=True)
        
        # File selection and Explain buttons in one frame
        code_buttons_frame = ttk.Frame(frame)
        code_buttons_frame.pack(pady=5)

        file_btn = ttk.Button(
            code_buttons_frame,
            text="Select Python File",
            style="Custom.TButton",
            command=self.select_code_file
        )
        file_btn.pack(side=tk.LEFT, padx=5)
        
        explain_btn = ttk.Button(
            code_buttons_frame,
            text="Explain Code",
            style="Custom.TButton",
            command=self.explain_code
        )
        explain_btn.pack(side=tk.LEFT, padx=5)
        
        # Explanation display
        self.explanation_display = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=('Helvetica', 11),
            background=self.secondary_color,
            foreground=self.text_color
        )
        self.explanation_display.pack(pady=10, padx=25, fill=tk.BOTH, expand=True)
        self.explanation_display.config(state=tk.DISABLED)
    
    def create_text_summarization_frame(self):
        """Create the text summarization interface"""
        frame = self.frames['text_summarization']
        
        # Back button
        back_btn = ttk.Button(
            frame,
            text="← Back to Home",
            style="Custom.TButton",
            command=lambda: self.show_frame('home')
        )
        back_btn.pack(pady=10, padx=10, anchor='w')
        
        # Title
        title_label = ttk.Label(
            frame,
            text="Text Summarization",
            font=('Helvetica', 20, 'bold')
        )
        title_label.pack(pady=10)
        
        # Text input area
        text_label = ttk.Label(frame, text="Enter your text:", font=('Helvetica', 12))
        text_label.pack(pady=5)
        
        self.text_input = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=70,
            height=10,
            font=('Helvetica', 10),
            background=self.secondary_color,
            foreground=self.text_color
        )
        self.text_input.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Summarize button
        summarize_btn = ttk.Button(
            frame,
            text="Summarize Text",
            style="Custom.TButton",
            command=self.summarize_text
        )
        summarize_btn.pack(pady=10)
        
        # Summary display
        self.summary_display = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=70,
            height=10,
            font=('Helvetica', 10),
            background=self.secondary_color,
            foreground=self.text_color
        )
        self.summary_display.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.summary_display.config(state=tk.DISABLED)

    def add_message(self, sender, message):
        """Add a message to the chat display with appropriate tags"""
        self.chat_display.config(state=tk.NORMAL)
        if sender == "You":
            self.chat_display.insert(tk.END, f"{message}\n", 'user')
        elif sender == "Assistant":
            self.chat_display.insert(tk.END, f"{message}\n", 'assistant')
        else: # System messages or errors
            self.chat_display.insert(tk.END, f"{message}\n", 'system')
        self.chat_display.insert(tk.END, "\n") # Add an extra newline for spacing between bubbles
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self, event=None):
        """Send message and get response"""
        message = self.message_input.get().strip()
        if not message:
            return
        
        # Clear input
        self.message_input.delete(0, tk.END)
        
        # Add user message to display
        self.add_message("You", message)
        
        # Disable input while processing
        self.message_input.config(state=tk.DISABLED)
        
        # Process message in a separate thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Process message and get response from chatbot"""
        try:
            response = self.chatbot.generate_response(message)
            self.root.after(0, lambda: self.add_message("Assistant", response))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("System", f"Error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.message_input.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.message_input.focus())
    
    def select_code_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not file_path:
            return
        code = read_python_file(file_path)
        if code is None:
            messagebox.showerror("Invalid File", "The selected file does not contain valid Python code.")
            return
        self.code_input.delete("1.0", tk.END)
        self.code_input.insert(tk.END, code)
    
    def explain_code(self):
        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Input Error", "Please enter some code to explain or select a file.")
            return

        self.explanation_display.config(state=tk.NORMAL)
        self.explanation_display.delete("1.0", tk.END)
        self.explanation_display.insert(tk.END, "Explaining code, please wait...")
        self.explanation_display.config(state=tk.DISABLED)

        threading.Thread(target=self._explain_code_thread, args=(code,)).start()

    def _explain_code_thread(self, code):
        try:
            explanation = get_code_explanation(code)
            self.root.after(0, self._update_explanation_display, explanation)
        except Exception as e:
            self.root.after(0, self._update_explanation_display, f"Error: {str(e)}")

    def _update_explanation_display(self, explanation):
        self.explanation_display.config(state=tk.NORMAL)
        self.explanation_display.delete("1.0", tk.END)
        self.explanation_display.insert(tk.END, explanation)
        self.explanation_display.config(state=tk.DISABLED)
    
    def summarize_text(self):
        """Summarize the input text using the Summarizer model"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to summarize.")
            return

        self.summary_display.config(state=tk.NORMAL)
        self.summary_display.delete("1.0", tk.END)
        self.summary_display.insert(tk.END, "Generating summary, please wait...")
        self.summary_display.config(state=tk.DISABLED)

        threading.Thread(target=self._summarize_text_thread, args=(text,)).start()

    def _summarize_text_thread(self, text):
        try:
            model = Summarizer()
            summary = model(text, ratio=0.3, min_length=30, max_length=150)
            self.root.after(0, self._update_summary_display, summary)
        except Exception as e:
            self.root.after(0, self._update_summary_display, f"Error: {str(e)}")

    def _update_summary_display(self, summary):
        self.summary_display.config(state=tk.NORMAL)
        self.summary_display.delete("1.0", tk.END)
        self.summary_display.insert(tk.END, summary)
        self.summary_display.config(state=tk.DISABLED)
    
    def show_frame(self, frame_name):
        """Show the selected frame and hide others"""
        for name, frame in self.frames.items():
            if name == frame_name:
                frame.tkraise()
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack_forget()

    def show_menu(self):
        """Show the menu popup with tool options"""
        menu = tk.Menu(self.root, tearoff=0)
        
        for tool_name, _, frame_name in self.tools:
            menu.add_command(
                label=tool_name,
                command=lambda f=frame_name: self.show_frame(f)
            )
        
        # Get the position of the menu button
        x = self.root.winfo_rootx() + 50
        y = self.root.winfo_rooty() + 50
        
        # Show the menu
        menu.post(x, y)

def main():
    root = tk.Tk()
    app = AIToolsHub(root)
    root.mainloop()

if __name__ == "__main__":
    main() 