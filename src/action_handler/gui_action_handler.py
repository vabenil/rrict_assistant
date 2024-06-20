import os
import sys

###### This is Ugly, but python decided this to be the *correct* way.
###### And who tf am I to question python design decisions?
# Get the absolute path to the package directory
package_path = os.path.abspath('../action_classifier/')
# Add the package path to sys.path
sys.path.append(package_path)

import torch
from intent_analysis.model2 import Net, run_model
from intent_analysis.label_manager import load_labels

import tkinter as tk
from tkinter import scrolledtext


def handle_action(input_text):
    labels_path = "../../labels.json"
    model_path = "../action_classifier/MODEL"

    model_labels = load_labels(labels_path)
    class_num = len(model_labels)
    model = Net.pretrained(class_num, model_path)

    label = run_model(model, [input_text], model_labels)[0]

    if label == "ALARM":
        return "opening alarm app"
    elif label == "CANCEL":
        return "cancelling request"
    elif label == "DATE":
        return "opening calendar app"
    elif label == "REPEAT":
        return "repeating request"
    elif label == "TIMER":
        return "opening timer app"
    elif label == "TRANSLATE":
        return "Starting translation"
    elif label == "WEATHER":
        return "opening weather app"
    elif label == "WHAT_CAN_I_ASK_YOU":
        return "I can help you with the following: \n" +\
              "1. Set an alarm \n" +\
              "2. doing calculations \n" +\
              "3. Check the date \n" +\
              "4. Repeat the last action \n" +\
              "5. Set a timer \n" +\
              "6. Translate a word \n" +\
              "7. Check the weather \n" +\
              "8. Talk to you \n" +\
              "9. Do web search \n" +\
              "10. Open calendar \n" +\
              "11. Do system actions \n" +\
              "12. Cancel requests \n"

    elif label == "CALCULATOR":
        return "opening calculator app"
    elif label == "WEB_SEARCH":
        return "doing web search"
    elif label == "YES":
        return "confirming"
    elif label == "NO":
        return "denying"
    elif label == "CALENDAR":
        return "opening calendar app"
    elif label == "SYSTEM_ACTION":
        return "doing system actions"
    elif label == "TALK_TO_ME":
        return "talking to you"

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Assistant")

        # Create a scrolled text widget for the conversation display
        self.conversation_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled')
        self.conversation_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create an entry widget for user input
        self.user_input = tk.Entry(master, width=100)
        self.user_input.pack(padx=10, pady=5, fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)

        # Create a send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def display_message(self, message, sender="You"):
        self.conversation_area.config(state='normal')
        self.conversation_area.insert(tk.END, f"{sender}: {message}\n")
        self.conversation_area.config(state='disabled')
        self.conversation_area.yview(tk.END)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip() == "":
            return

        self.display_message(user_message, "You")
        self.user_input.delete(0, tk.END)

        # Call the chatbot function here
        bot_response = self.get_bot_response(user_message)
        self.display_message(bot_response, "Bot")

    def get_bot_response(self, message):
        return handle_action(message)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()
