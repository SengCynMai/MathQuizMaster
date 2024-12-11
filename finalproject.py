import random
import csv
from tkinter import Tk, Label, Button, Frame, Toplevel
from pygame import mixer  # For background music


class MathQuizMaster:
    def __init__(self):
        self.score = 0
        self.level = "easy"
        self.current_question = ""
        self.correct_answer = None
        self.options = []
        self.total_time = 60  # Total game time in seconds
        self.leaderboard_file = "leaderboard.csv"  # File to store scores

        # Initialize the GUI
        self.root = Tk()
        self.root.title("Math Quiz Master")

        # Full-screen mode
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#AEE6D8")  # Mint background color

        # Play background music
        self.start_bgm()

        # Main frame for centering
        self.main_frame = Frame(self.root, bg="#AEE6D8")
        self.main_frame.pack(expand=True)

        # Title and buttons
        self.title_label = Label(
            self.main_frame,
            text="Math Quiz Master",
            font=("Comic Sans MS", 40, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        )
        self.title_label.pack(pady=20)

        self.start_button = Button(
            self.main_frame,
            text="Start Game",
            font=("Comic Sans MS", 20),
            bg="#FFD1DC",
            fg="#000000",
            activebackground="#FFB3C1",
            activeforeground="#000000",
            command=self.start_game,
            relief="groove"
        )
        self.start_button.pack(pady=10)

        self.about_button = Button(
            self.main_frame,
            text="About",
            font=("Comic Sans MS", 20),
            bg="#FFD1DC",
            fg="#000000",
            activebackground="#FFB3C1",
            activeforeground="#000000",
            command=self.show_about,
            relief="groove"
        )
        self.about_button.pack(pady=10)

        # Game screen widgets
        self.game_frame = Frame(self.root, bg="#AEE6D8")
        self.question_label = Label(
            self.game_frame,
            text="",
            font=("Comic Sans MS", 24, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        )
        self.timer_label = Label(
            self.game_frame,
            text="",
            font=("Comic Sans MS", 18),
            bg="#AEE6D8",
            fg="#333333"
        )
        self.score_label = Label(
            self.game_frame,
            text="",
            font=("Comic Sans MS", 18, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        )

        self.feedback_label = Label(
            self.game_frame,
            text="",
            font=("Comic Sans MS", 20),
            bg="#AEE6D8",
            fg="#000000"
        )

        self.option_frame = Frame(self.game_frame, bg="#AEE6D8")
        self.option_buttons = []
        for i in range(4):
            button = Button(
                self.option_frame,
                text="",
                font=("Comic Sans MS", 16),
                bg="#88D4CC",
                fg="#000000",
                activebackground="#AED581",
                activeforeground="#000000",
                width=15,
                height=2,
                command=lambda i=i: self.on_option_click(i),
                relief="ridge",
                bd=3
            )
            button.grid(row=i // 2, column=i % 2, padx=30, pady=20)
            self.option_buttons.append(button)

        # End screen widgets
        self.end_frame = Frame(self.root, bg="#AEE6D8")

        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)
        self.root.mainloop()

    def start_bgm(self):
        try:
            mixer.init()
            mixer.music.load("bgm.mp3")  # Replace with your BGM file path
            mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Error playing BGM: {e}")

    def start_game(self):
        self.main_frame.pack_forget()  # Hide initial screen

        # Show game frame
        self.game_frame.pack(expand=True)
        self.question_label.pack(pady=10)
        self.timer_label.pack()
        self.score_label.pack()
        self.feedback_label.pack(pady=10)
        self.option_frame.pack(pady=20)

        self.score = 0
        self.level = "easy"
        self.total_time = 60
        self.start_timer()
        self.next_question()

    def next_question(self):
        if self.score >= 10:
            self.level = "medium"
        if self.score >= 20:
            self.level = "hard"

        self.generate_question()
        self.question_label.config(text=f"Question: {self.current_question}")
        self.score_label.config(text=f"Score: {self.score}")
        self.feedback_label.config(text="")  # Clear feedback

        for i, option in enumerate(self.options):
            self.option_buttons[i].config(text=str(option), state="normal", bg="#88D4CC")

    def start_timer(self):
        if self.total_time > 0:
            self.total_time -= 1
            self.timer_label.config(text=f"Time left: {self.total_time}s")
            self.root.after(1000, self.start_timer)
        else:
            self.end_game()

    def on_option_click(self, selected_index):
        if self.options[selected_index] == self.correct_answer:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="#388E3C")  # Green for correct
        else:
            self.feedback_label.config(text="Incorrect!", fg="#D32F2F")  # Red for incorrect

        for button in self.option_buttons:
            button.config(state="disabled")

        self.root.after(300, self.next_question)  # Delay for feedback before next question

    def end_game(self):
        self.game_frame.pack_forget()  # Hide game screen

        # Reset the end frame
        self.end_frame.pack_forget()
        self.end_frame = Frame(self.root, bg="#AEE6D8")
        self.end_frame.pack(expand=True)

        Label(
            self.end_frame,
            text="Time's Up!",
            font=("Comic Sans MS", 30, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        ).pack(pady=20)
        Label(
            self.end_frame,
            text=f"Your Score: {self.score}",
            font=("Comic Sans MS", 24, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        ).pack(pady=10)

        Button(
            self.end_frame,
            text="Restart Game",
            font=("Comic Sans MS", 16, "bold"),
            bg="#FFD1DC",
            fg="#000000",
            activebackground="#FFB3C1",
            activeforeground="#000000",
            command=self.restart_game,
            relief="groove"
        ).pack(pady=10)

        Button(
            self.end_frame,
            text="Show Leaderboard",
            font=("Comic Sans MS", 16, "bold"),
            bg="#FFD1DC",
            fg="#000000",
            activebackground="#FFB3C1",
            activeforeground="#000000",
            command=self.show_leaderboard,
            relief="groove"
        ).pack(pady=10)

        Button(
            self.end_frame,
            text="Home",
            font=("Comic Sans MS", 16, "bold"),
            bg="#FFD1DC",
            fg="#000000",
            activebackground="#FFB3C1",
            activeforeground="#000000",
            command=self.go_home,
            relief="groove"
        ).pack(pady=10)

        self.save_score()

    def restart_game(self):
        self.end_frame.pack_forget()
        self.start_game()

    def show_leaderboard(self):
        leaderboard_window = Toplevel(self.root)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("400x400")
        leaderboard_window.configure(bg="#AEE6D8")

        Label(
            leaderboard_window,
            text="Leaderboard",
            font=("Comic Sans MS", 20, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        ).pack(pady=20)

        try:
            with open(self.leaderboard_file, "r") as file:
                reader = csv.reader(file)
                scores = sorted([int(row[0]) for row in reader], reverse=True)
                leaderboard_text = "\n".join([f"{i+1}. {score}" for i, score in enumerate(scores[:5])])
        except FileNotFoundError:
            leaderboard_text = "No leaderboard data available."

        Label(
            leaderboard_window,
            text=leaderboard_text,
            font=("Comic Sans MS", 16),
            bg="#AEE6D8",
            fg="#000000",
            justify="center",
            wraplength=350
        ).pack(pady=10)

        Button(
            leaderboard_window,
            text="Close",
            font=("Comic Sans MS", 14),
            bg="#FFD1DC",
            fg="#000000",
            command=leaderboard_window.destroy
        ).pack(pady=20)

    def go_home(self):
        self.end_frame.pack_forget()
        if hasattr(self, 'game_frame'):
            self.game_frame.pack_forget()
        self.main_frame.pack(expand=True)

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("About Math Quiz Master")
        about_window.geometry("400x400")
        about_window.configure(bg="#AEE6D8")
        Label(
            about_window,
            text="About Math Quiz Master",
            font=("Comic Sans MS", 18, "bold"),
            bg="#AEE6D8",
            fg="#000000"
        ).pack(pady=10)
        Label(
            about_window,
            text=(
                "Test your math skills with exciting questions. Solve as many as you can in 60 seconds.\n"
                "Progress through increasing difficulty levels as you score higher.\n"
                "Compete to achieve the highest score!"
            ),
            font=("Comic Sans MS", 14),
            bg="#AEE6D8",
            fg="#000000",
            wraplength=350,
            justify="center"
        ).pack(expand=True, pady=20)
        Button(
            about_window,
            text="Close",
            font=("Comic Sans MS", 14),
            bg="#FFD1DC",
            fg="#000000",
            command=about_window.destroy
        ).pack(pady=20)

    def generate_question(self):
        operations = {
            "easy": ["+", "-"],
            "medium": ["*", "/"],
            "hard": ["*", "/"]
        }
        op = random.choice(operations[self.level])
        a, b = random.randint(1, 10), random.randint(1, 10)
        if op == "-":
            a, b = max(a, b), min(a, b)  # Ensure positive result for subtraction
        if op == "/":
            a, b = a * b, b  # Ensure division yields a positive integer
        self.current_question = f"{a} {op} {b}"
        self.correct_answer = int(eval(self.current_question))

        incorrect_answers = set()
        while len(incorrect_answers) < 3:
            incorrect = self.correct_answer + random.randint(1, 10)
            if incorrect != self.correct_answer:
                incorrect_answers.add(incorrect)
        self.options = list(incorrect_answers) + [self.correct_answer]
        random.shuffle(self.options)

    def save_score(self):
        try:
            with open(self.leaderboard_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.score])
        except Exception as e:
            print(f"Error saving score: {e}")

    def save_and_exit(self):
        self.root.destroy()


# Run the game
MathQuizMaster()
