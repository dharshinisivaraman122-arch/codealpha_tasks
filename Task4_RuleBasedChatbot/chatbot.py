"""
=============================================================
  Task 4 — Rule-Based Chatbot
  Tech  : Python 3 + Tkinter (standard library, no installs)
  Author: Dharshini
=============================================================

README
------
This is a GUI-based rule-based chatbot built as an internship
mini-project. It demonstrates the following core Python concepts:

  1. if-elif-else  — every reply is chosen by a chain of conditions
  2. Functions     — get_response() isolates the reply logic cleanly
  3. Loops         — the Tkinter event loop replaces 'while True'
  4. Input/Output  — entry widget = input, chat area = output

HOW TO RUN
----------
  python chatbot.py          (Python 3.8 or newer)

No third-party libraries needed — only the Python standard library.

FEATURES
--------
  • Greetings, wellbeing, identity, time/date replies
  • Explains Python, AI, and Machine Learning in simple terms
  • Tells a random joke on demand
  • Motivational quote on request
  • Save chat history to a .txt file
  • Clear chat with one click
  • Colour-coded Bot (blue) vs You (green) messages
=============================================================
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, filedialog
from datetime import datetime
import random  # used for random jokes and quotes


# ─────────────────────────────────────────────────────────────
#  JOKE & QUOTE BANKS  (add more anytime!)
# ─────────────────────────────────────────────────────────────
JOKES = [
    "Why do programmers prefer dark mode?\n  Because light attracts bugs! 🐛",
    "Why did the Python programmer get cold?\n  Because they left their Windows open! 🪟",
    "How many programmers does it take to change a light bulb?\n  None — that's a hardware problem! 💡",
    "Why do Java developers wear glasses?\n  Because they don't C#! 😄",
    "What's a computer's favourite snack?\n  Microchips! 🍟",
]

QUOTES = [
    "\"The only way to do great work is to love what you do.\" — Steve Jobs",
    "\"Code is like humour. When you have to explain it, it's bad.\" — Cory House",
    "\"First, solve the problem. Then, write the code.\" — John Johnson",
    "\"Programs must be written for people to read.\" — Harold Abelson",
    "\"Learning never exhausts the mind.\" — Leonardo da Vinci",
]


# ─────────────────────────────────────────────────────────────
#  TYPO-TOLERANCE HELPER
#  Checks if any keyword from a list appears anywhere in text.
#  This gives partial / fuzzy matching without extra libraries.
# ─────────────────────────────────────────────────────────────
def contains_any(text: str, keywords: list) -> bool:
    """Return True if ANY keyword is found inside text."""
    return any(kw in text for kw in keywords)


# ─────────────────────────────────────────────────────────────
#  CORE REPLY FUNCTION
#  Key Concept: if-elif chain + function
#  Each branch checks the user's message and returns a reply.
# ─────────────────────────────────────────────────────────────
def get_response(user_text: str) -> str:
    """
    Match user_text against predefined rules and return a reply.
    .lower().strip() gives basic case-insensitive + whitespace tolerance.
    """
    # Normalise input — case-insensitive and trimmed (typo tolerance)
    text = user_text.lower().strip()

    # ── 1. Greetings ──────────────────────────────────────────
    if contains_any(text, ["hello", "hi", "hey", "good morning", "good evening", "howdy"]):
        return "Hi! 👋 How can I help you today?"

    # ── 2. Wellbeing ──────────────────────────────────────────
    elif contains_any(text, ["how are you", "how r you", "hows you", "you ok"]):
        return "I'm fine, thanks! 😊 How about you?"

    # ── 3. Bot identity ───────────────────────────────────────
    elif contains_any(text, ["your name", "who are you", "what are you", "introduce"]):
        return (
            "I'm a rule-based chatbot built with Python & Tkinter! 🤖\n"
            "I reply using if-elif logic — no fancy AI needed."
        )

    # ── 4. What is Python? ────────────────────────────────────
    elif contains_any(text, ["what is python", "tell me about python", "explain python",
                              "python language", "about python"]):
        return (
            "🐍 Python is a high-level, beginner-friendly programming language.\n"
            "It is used in:\n"
            "  • Web development (Django, Flask)\n"
            "  • Data Science & AI (NumPy, Pandas, TensorFlow)\n"
            "  • Automation & scripting\n"
            "  • GUI apps — like this chatbot!\n"
            "It is famous for its clean, readable syntax."
        )

    # ── 5. What is AI? ────────────────────────────────────────
    elif contains_any(text, ["what is ai", "artificial intelligence", "tell me about ai",
                              "explain ai", "what is artificial"]):
        return (
            "🤖 Artificial Intelligence (AI) is the simulation of human\n"
            "intelligence in machines. It includes:\n"
            "  • Machine Learning — learning from data\n"
            "  • Natural Language Processing — understanding text\n"
            "  • Computer Vision — understanding images\n"
            "Fun fact: this chatbot uses simple rule-based AI!"
        )

    # ── 6. What is Machine Learning? ─────────────────────────
    elif contains_any(text, ["machine learning", "what is ml", "deep learning", "neural"]):
        return (
            "📊 Machine Learning (ML) is a branch of AI where machines\n"
            "learn patterns from data instead of being explicitly programmed.\n"
            "Example: teaching a model to recognise cats in photos by\n"
            "showing it thousands of cat images."
        )

    # ── 7. Tell a joke ────────────────────────────────────────
    elif contains_any(text, ["joke", "funny", "laugh", "make me laugh", "tell me something funny"]):
        return "😄 " + random.choice(JOKES)

    # ── 8. Motivational quote ─────────────────────────────────
    elif contains_any(text, ["quote", "motivat", "inspire", "encourage", "wisdom"]):
        return "✨ " + random.choice(QUOTES)

    # ── 9. Time ───────────────────────────────────────────────
    elif "time" in text:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}. ⏰"

    # ── 10. Date ──────────────────────────────────────────────
    elif "date" in text or "today" in text:
        return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}. 📅"

    # ── 11. Thank you ─────────────────────────────────────────
    elif contains_any(text, ["thank", "thanks", "thx", "ty"]):
        return "You're welcome! 😊 Happy to help."

    # ── 12. Help menu ─────────────────────────────────────────
    elif "help" in text:
        return (
            "Here's what I understand:\n"
            "  • hello / hi / hey\n"
            "  • how are you\n"
            "  • who are you\n"
            "  • what is python\n"
            "  • what is AI\n"
            "  • machine learning\n"
            "  • tell me a joke\n"
            "  • give me a quote\n"
            "  • time  /  date\n"
            "  • bye"
        )

    # ── 13. Farewell ──────────────────────────────────────────
    elif contains_any(text, ["bye", "goodbye", "exit", "quit", "see you", "take care"]):
        return "Goodbye! 👋 Have a great day!"

    # ── 14. Default fallback ──────────────────────────────────
    else:
        return (
            "🤔 Sorry, I didn't understand that.\n"
            "Type 'help' to see the commands I know."
        )


# ─────────────────────────────────────────────────────────────
#  GUI CHATBOT CLASS
#  Builds the Tkinter window, chat area, input box, and buttons.
#  All user interaction flows through _on_send() which calls
#  get_response() and displays results — input → process → output.
# ─────────────────────────────────────────────────────────────
class ChatbotApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Rule-Based Chatbot")
        self.root.geometry("700x560")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.chat_history: list[str] = []

        self._build_header()
        self._build_chat_area()
        self._build_input_area()
        self._build_footer()

        # Welcome message (Key Concept: output)
        self._show_message("Bot", "Hello! I'm your rule-based chatbot. Type 'help' to get started.")

    # ── Layout builders ───────────────────────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self.root, bg="#1e293b", height=58)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="💬  SIMPLE CHATBOT",
            font=("Helvetica", 18, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(pady=14)

    def _build_chat_area(self):
        frame = tk.Frame(self.root, bg="#0f172a")
        frame.pack(padx=14, pady=(10, 4), fill=tk.BOTH, expand=True)

        self.chat_area = ScrolledText(
            frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="#f8fafc",
            fg="#0f172a",
            state="disabled",
            padx=10,
            pady=10,
            relief=tk.FLAT,
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        # Colour tags for sender labels
        self.chat_area.tag_config("bot_label",  foreground="#2563eb", font=("Arial", 12, "bold"))
        self.chat_area.tag_config("user_label", foreground="#16a34a", font=("Arial", 12, "bold"))
        self.chat_area.tag_config("body",       foreground="#1e293b", font=("Arial", 12))
        self.chat_area.tag_config("time",       foreground="#94a3b8", font=("Arial", 10))

    def _build_input_area(self):
        frame = tk.Frame(self.root, bg="#0f172a")
        frame.pack(fill=tk.X, padx=14, pady=8)

        self.entry = tk.Entry(
            frame,
            font=("Arial", 13),
            bg="#ffffff",
            fg="#0f172a",
            relief=tk.FLAT,
            insertbackground="#0f172a",
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9, padx=(0, 8))
        self.entry.bind("<Return>", self._on_send)   # Key Concept: loops via event binding
        self.entry.focus_set()

        for label, color, active, cmd in [
            ("Send",  "#22c55e", "#16a34a", self._on_send),
            ("Clear", "#ef4444", "#dc2626", self._clear_chat),
            ("Save",  "#3b82f6", "#2563eb", self._save_chat),
        ]:
            tk.Button(
                frame,
                text=label,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                activebackground=active,
                activeforeground="white",
                width=8,
                relief=tk.FLAT,
                cursor="hand2",
                command=cmd,
            ).pack(side=tk.LEFT, padx=(0, 6))

    def _build_footer(self):
        tk.Label(
            self.root,
            text="Task 4 — Rule-Based Chatbot  |  Python & Tkinter",
            font=("Arial", 9),
            bg="#1e293b",
            fg="#94a3b8",
            pady=6,
        ).pack(fill=tk.X, side=tk.BOTTOM)

    # ── Core logic ────────────────────────────────────────────────────────────

    def _show_message(self, sender: str, message: str):
        """Append a styled message to the chat area."""
        timestamp = datetime.now().strftime("%I:%M %p")
        self.chat_area.config(state="normal")

        tag = "bot_label" if sender == "Bot" else "user_label"
        self.chat_area.insert(tk.END, f"{sender} ", tag)
        self.chat_area.insert(tk.END, f"[{timestamp}]\n", "time")
        self.chat_area.insert(tk.END, f"{message}\n\n", "body")

        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

        # Keep history for saving
        self.chat_history.append(f"{sender} [{timestamp}]: {message}\n\n")

    def _on_send(self, event=None):
        """Handle Send button / Enter key — the main input/output loop."""
        user_msg = self.entry.get().strip()
        if not user_msg:
            messagebox.showwarning("Empty Input", "Please type a message first.")
            return

        self._show_message("You", user_msg)            # Key Concept: output
        reply = get_response(user_msg)                 # Key Concept: function call
        self._show_message("Bot", reply)               # Key Concept: output

        self.entry.delete(0, tk.END)

        # Auto-close after farewell
        if user_msg.lower() in ["bye", "goodbye", "exit", "quit"]:
            self.root.after(1500, self.root.destroy)

    def _clear_chat(self):
        if messagebox.askyesno("Clear Chat", "Clear all messages?"):
            self.chat_area.config(state="normal")
            self.chat_area.delete("1.0", tk.END)
            self.chat_area.config(state="disabled")
            self.chat_history.clear()
            self._show_message("Bot", "Chat cleared. How can I help you?")

    def _save_chat(self):
        if not self.chat_history:
            messagebox.showinfo("Save Chat", "Nothing to save yet.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Chat History",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(self.chat_history)
            messagebox.showinfo("Save Chat", "Chat saved successfully!")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()
