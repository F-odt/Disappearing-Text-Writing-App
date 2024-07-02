import tkinter as tk
from tkinter import messagebox
import random


class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disappearing Text Writing App 📝")

        # Style configuration
        self.bg_color = "#F1F8E8"  # Background color for the window
        self.text_bg_color = "#FFFFFF"  # Background color for the text box
        self.text_color = "#000000"  # Default text color
        self.user_input_color = "#FF5733"  # Color for user input text
        self.centered_font = ("Helvetica", 14)  # Font for centered text
        self.timer_font = ("Helvetica", 12, "bold")  # Font for the timer label
        self.button_font = ("Helvetica", 12)  # Font for buttons
        self.word_count_font = ("Helvetica", 12, "bold")  # Font for word count label

        self.root.configure(bg=self.bg_color)

        # Create a frame to hold the text and center it
        self.frame = tk.Frame(root, bg=self.bg_color)
        self.frame.pack(expand=True, pady=20)

        # Create a text widget for user input and sample sentence
        self.text = tk.Text(self.frame, wrap=tk.WORD, font=self.centered_font,
                            width=50, height=15, bg=self.text_bg_color, fg=self.text_color)
        self.text.tag_configure("center", justify='center')  # Center the text
        self.text.tag_configure("user_input", foreground=self.user_input_color,
                                justify='center')  # Style for user input text
        self.text.pack(expand=True, padx=20, pady=20)

        # Label to display the word count
        self.word_count_label = tk.Label(root, text="0 words",
                                         font=self.word_count_font, bg=self.bg_color, fg="#55AD9B")
        self.word_count_label.pack(pady=5)

        # Start/Stop button
        self.start_stop_button = tk.Button(root, text="Start", command=self.start_stop,
                                           font=self.button_font, bg="#55AD9B", fg="#FFFFFF",
                                           activebackground="#95D2B3", activeforeground="#FFFFFF")
        self.start_stop_button.pack(pady=10)

        # Label to display the countdown timer
        self.timer_label = tk.Label(root, text="Time left: 5", font=self.timer_font, bg=self.bg_color, fg="#55AD9B")
        self.timer_label.pack(pady=5)

        # Load sample sentences from file
        self.samples = self.load_samples("samples.txt")
        self.current_sample = ""
        self.timer = 5  # Initial timer value
        self.running = False  # Flag to check if the app is running
        self.fading = False  # Flag to check if the text is fading
        self.word_count = 0  # Initial word count

        # Bind key events to reset the timer and update the word count
        self.root.bind('<Key>', self.reset_timer)
        self.root.bind('<KeyRelease>', self.update_word_count)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_samples(self, filepath):
        """Load sample sentences from a text file."""
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                if not lines:
                    raise ValueError("The samples file is empty.")
                return [line.strip() for line in lines if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Error loading samples: {e}")
            self.root.quit()

    def start_stop(self):
        """Toggle between starting and stopping the app."""
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        """Start the app, load a new sentence, and reset the timer."""
        self.running = True
        self.start_stop_button.config(text="Stop")
        self.load_new_sentence()
        self.reset_timer()
        self.countdown()

    def stop(self):
        """Stop the app, clear the text, and reset the timer and word count."""
        self.running = False
        self.start_stop_button.config(text="Start")
        self.text.delete(1.0, tk.END)
        self.timer_label.config(text="Time left: 5")
        self.word_count_label.config(text="0 words")
        self.timer = 5
        self.word_count = 0

    def reset_timer(self, event=None):
        """Reset the countdown timer to 5 seconds and apply user input styling."""
        if self.running:
            self.timer = 5
            self.timer_label.config(text=f"Time left: {self.timer}")

            # Apply user input color to the text after the initial sentence and center the user's input
            self.text.tag_add("user_input", "end-1c linestart", "end-1c")
            self.text.tag_add("center", "end-1c linestart", "end-1c")

    def update_word_count(self, event=None):
        """Update the word count based on the user's input."""
        if self.running:
            content = self.text.get("1.0", tk.END).strip()
            words = content.split()
            original_words = self.current_sample.split()
            self.word_count = len(original_words) + len(words)
            self.word_count_label.config(text=f"{self.word_count} words")

    def countdown(self):
        """Countdown the timer and handle timer expiration."""
        if self.running:
            if self.timer > 0:
                self.timer -= 1
                self.timer_label.config(text=f"Time left: {self.timer}")
                self.root.after(1000, self.countdown)
            else:
                self.start_fading()

    def start_fading(self):
        """Start fading the text color to indicate time out."""
        if self.running:
            self.fading = True
            self.text.tag_configure("fade", foreground="gray")
            self.fade_text()

    def fade_text(self):
        """Gradually fade the text color until it becomes black and delete the text."""
        if self.fading:
            current_opacity = self.text.tag_cget("fade", "foreground")
            new_opacity = self.decrease_opacity(current_opacity)
            self.text.tag_configure("fade", foreground=new_opacity)
            self.text.tag_add("fade", 1.0, tk.END)
            if new_opacity != "black":
                self.root.after(500, self.fade_text)
            else:
                self.delete_text()

    def decrease_opacity(self, color):
        """Helper function to decrease the opacity of the text color."""
        if color == "gray":
            return "dark gray"
        elif color == "dark gray":
            return "black"
        else:
            return "black"

    def delete_text(self):
        """Delete all text and load a new sentence after a delay."""
        self.text.delete(1.0, tk.END)
        self.fading = False
        self.word_count_label.config(text="0 words")
        self.word_count = 0
        self.root.after(2000, self.load_new_sentence)

    def load_new_sentence(self):
        """Load a new random sentence from the samples and reset the timer."""
        if self.samples:
            self.current_sample = random.choice(self.samples)
            self.text.insert(tk.END, self.current_sample + "\n\n", "center")
            self.reset_timer()
            self.countdown()

    def on_closing(self):
        """Handle the window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.running = False
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()
