import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

QUESTIONS = [
    {
        "question": "How many players from one team are on the court during a regular indoor volleyball match?",
        "choices": ["A. 5 players", "B. 6 players", "C. 7 players", "D. 8 players"],
        "answer": "B"
    },
    {
        "question": "How many times may a team usually touch the ball before sending it over the net?",
        "choices": ["A. 2 touches", "B. 4 touches", "C. 3 touches", "D. 5 touches"],
        "answer": "C"
    },
    {
        "question": "What is the name of the player who specializes in back-row defense and wears a different-colored jersey?",
        "choices": ["A. Setter", "B. Middle blocker", "C. Outside hitter", "D. Libero"],
        "answer": "D"
    },
    {
        "question": "What is the standard number of points needed to win a regular set (excluding a deciding fifth set)?",
        "choices": ["A. 25 points", "B. 15 points", "C. 21 points", "D. 30 points"],
        "answer": "A"
    },
    {
        "question": "Which skill is commonly used to receive a serve?",
        "choices": ["A. Spike", "B. Forearm pass", "C. Block", "D. Jump serve"],
        "answer": "B"
    },
    {
        "question": "What is the player called who usually sets up the team's attackers?",
        "choices": ["A. Libero", "B. Opposite", "C. Setter", "D. Defensive specialist"],
        "answer": "C"
    },
    {
        "question": "What action starts a rally in volleyball?",
        "choices": ["A. Serve", "B. Block", "C. Dig", "D. Set"],
        "answer": "A"
    },
    {
        "question": "When a team wins the right to serve from the opposing team, what does it do?",
        "choices": ["A. Substitutes every player", "B. Changes court size", "C. Takes a timeout", "D. Rotates one position clockwise"],
        "answer": "D"
    },
    {
        "question": "What is an attack hit that sends the ball forcefully down into the opponent's court commonly called?",
        "choices": ["A. Set", "B. Spike", "C. Pass", "D. Float"],
        "answer": "B"
    },
    {
        "question": "What happens when the ball lands on a boundary line?",
        "choices": ["A. It is out", "B. The rally is replayed", "C. It is considered in", "D. The serving team loses a point"],
        "answer": "C"
    }
]

TIME_LIMIT = 15
TOTAL_QUESTIONS = len(QUESTIONS)
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "volleyvibe_high_score.txt")

BG = "#F4EEFF"
PANEL = "#FFFFFF"
DARK_PURPLE = "#3B176B"
PURPLE = "#6D35A8"
MID_PURPLE = "#8B5CC7"
LIGHT_PURPLE = "#E8D9FA"
PALE_PURPLE = "#F8F3FF"
TEXT = "#28143D"
MUTED = "#705D82"
GREEN = "#23834B"
GREEN_BG = "#E2F6E9"
RED = "#C43D58"
RED_BG = "#FCE7EC"
GOLD = "#D69B24"

root = tk.Tk()
root.title("VolleyVibe | Volleyball Challenge")
root.geometry("900x720")
root.minsize(820, 660)
root.configure(bg=BG)
root.resizable(True, True)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Purple.Horizontal.TProgressbar",
    troughcolor=LIGHT_PURPLE,
    background=PURPLE,
    bordercolor=LIGHT_PURPLE,
    lightcolor=PURPLE,
    darkcolor=PURPLE,
    thickness=13
)

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=28, pady=22)


quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
player_name = ""
selected_answer = tk.StringVar()

timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []
progress_bar = None
progress_label = None


def get_high_score():
    """Read the saved high score from the text file."""
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError, OSError):
        return 0


def save_high_score(new_score):
    """Save a new high score only when it beats the previous record."""
    if new_score > get_high_score():
        try:
            with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
                file.write(str(new_score))
            return True
        except OSError:
            messagebox.showwarning("Saving issue", "The high score could not be saved.")
    return False


def clear_screen():
    """Remove all widgets from the main content frame."""
    for widget in main_frame.winfo_children():
        widget.destroy()


def make_button(parent, text, command, color=PURPLE, width=16):
    """Create a consistently styled rounded-looking Tkinter button."""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=color,
        fg="white",
        activebackground=MID_PURPLE,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        width=width,
        cursor="hand2"
    )
    return button


def get_choice_text(question, letter):
    """Return the complete choice text that matches a letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"

def show_start_screen():
    clear_screen()

    header = tk.Frame(main_frame, bg=DARK_PURPLE, padx=25, pady=22)
    header.pack(fill="x", pady=(0, 18))

    tk.Label(
        header, text="VOLLEYVIBE", font=("Segoe UI", 27, "bold"),
        bg=DARK_PURPLE, fg="white"
    ).pack(anchor="w")

    tk.Label(
        header, text="THE ULTIMATE VOLLEYBALL CHALLENGE",
        font=("Segoe UI", 10, "bold"), bg=DARK_PURPLE, fg="#E5D2FF"
    ).pack(anchor="w", pady=(3, 0))

    card = tk.Frame(main_frame, bg=PANEL, padx=32, pady=25,
                    highlightthickness=1, highlightbackground=LIGHT_PURPLE)
    card.pack(fill="both", expand=True)

    tk.Label(
        card, text="Ready to take the court?",
        font=("Segoe UI", 21, "bold"), bg=PANEL, fg=DARK_PURPLE
    ).pack(pady=(4, 6))

    tk.Label(
        card, text="Test your volleyball knowledge, one question at a time.",
        font=("Segoe UI", 11), bg=PANEL, fg=MUTED
    ).pack(pady=(0, 20))

    tk.Label(
        card, text="PLAYER NAME", font=("Segoe UI", 10, "bold"),
        bg=PANEL, fg=PURPLE
    ).pack(anchor="w", padx=105)

    name_entry = tk.Entry(
        card, font=("Segoe UI", 13), justify="center",
        bg=PALE_PURPLE, fg=TEXT, insertbackground=TEXT,
        relief="flat", highlightthickness=2,
        highlightbackground=LIGHT_PURPLE, highlightcolor=PURPLE
    )
    name_entry.pack(fill="x", padx=105, ipady=10, pady=(7, 18))
    name_entry.insert(0, "")

    info = tk.Frame(card, bg=PALE_PURPLE, padx=18, pady=14)
    info.pack(fill="x", padx=70, pady=(0, 17))

    tk.Label(
        info, text=f"{TOTAL_QUESTIONS} QUESTIONS",
        font=("Segoe UI", 10, "bold"), bg=PALE_PURPLE, fg=DARK_PURPLE
    ).pack(side="left", expand=True)

    tk.Label(
        info, text=f"{TIME_LIMIT} SECONDS EACH",
        font=("Segoe UI", 10, "bold"), bg=PALE_PURPLE, fg=DARK_PURPLE
    ).pack(side="left", expand=True)

    tk.Label(
        card, text=f"PERSONAL BEST: {get_high_score()} / {TOTAL_QUESTIONS}",
        font=("Segoe UI", 11, "bold"), bg=PANEL, fg=GOLD
    ).pack(pady=(0, 14))

    def begin():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name before starting.")
            name_entry.focus_set()
            return
        global player_name
        player_name = name
        start_quiz()

    make_button(card, "START CHALLENGE  ➜", begin, DARK_PURPLE, 22).pack(pady=4)
    name_entry.bind("<Return>", lambda event: begin())
    name_entry.focus_set()

    tk.Label(
        main_frame, text="VOLLEYVIBE  •  PLAY SMART. PLAY TOGETHER.",
        font=("Segoe UI", 9, "bold"), bg=BG, fg=MUTED
    ).pack(pady=(13, 0))


def start_quiz():
    """Reset the quiz and shuffle all questions for a new round."""
    global quiz_questions, current_question, score, wrong_answers
    stop_timer()
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


def show_question():
    """Build the question screen and start its countdown."""
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons
    global progress_bar, progress_label

    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    top = tk.Frame(main_frame, bg=DARK_PURPLE, padx=20, pady=15)
    top.pack(fill="x", pady=(0, 15))

    tk.Label(
        top, text="VOLLEYVIBE", font=("Segoe UI", 15, "bold"),
        bg=DARK_PURPLE, fg="white"
    ).pack(side="left")

    timer_label = tk.Label(
        top, text=f"TIME: {TIME_LIMIT}s", font=("Segoe UI", 12, "bold"),
        bg=DARK_PURPLE, fg="#FFE59A"
    )
    timer_label.pack(side="right")

    details = tk.Frame(main_frame, bg=BG)
    details.pack(fill="x", pady=(0, 7))

    progress_label = tk.Label(
        details, text=f"QUESTION {current_question + 1} OF {TOTAL_QUESTIONS}",
        font=("Segoe UI", 11, "bold"), bg=BG, fg=DARK_PURPLE
    )
    progress_label.pack(side="left")

    tk.Label(
        details, text=f"PLAYER: {player_name}     •     SCORE: {score}",
        font=("Segoe UI", 10, "bold"), bg=BG, fg=MUTED
    ).pack(side="right")

    progress_bar = ttk.Progressbar(
        main_frame, style="Purple.Horizontal.TProgressbar",
        maximum=TOTAL_QUESTIONS, value=current_question
    )
    progress_bar.pack(fill="x", pady=(0, 18))

    card = tk.Frame(
        main_frame, bg=PANEL, padx=28, pady=25,
        highlightthickness=1, highlightbackground=LIGHT_PURPLE
    )
    card.pack(fill="both", expand=True)

    tk.Label(
        card, text="🏐  VOLLEYBALL KNOWLEDGE",
        font=("Segoe UI", 10, "bold"), bg=PANEL, fg=MID_PURPLE
    ).pack(anchor="w", pady=(0, 13))

    tk.Label(
        card, text=question["question"],
        font=("Segoe UI", 17, "bold"), wraplength=760,
        justify="left", bg=PANEL, fg=TEXT
    ).pack(anchor="w", pady=(0, 22))

    choices_frame = tk.Frame(card, bg=PANEL)
    choices_frame.pack(fill="x")

    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        rb = tk.Radiobutton(
            choices_frame,
            text=choice,
            variable=selected_answer,
            value=letter,
            font=("Segoe UI", 12),
            bg=PALE_PURPLE,
            fg=TEXT,
            activebackground=LIGHT_PURPLE,
            activeforeground=DARK_PURPLE,
            selectcolor=LIGHT_PURPLE,
            anchor="w",
            padx=15,
            pady=12,
            relief="flat",
            indicatoron=True,
            highlightthickness=1,
            highlightbackground=LIGHT_PURPLE,
            wraplength=700,
            justify="left"
        )
        rb.pack(fill="x", pady=5)
        choice_buttons.append(rb)

    feedback_label = tk.Label(
        card, text="Choose the best answer, then submit.",
        font=("Segoe UI", 11, "bold"), bg=PANEL, fg=MUTED,
        wraplength=740, justify="left"
    )
    feedback_label.pack(anchor="w", pady=(15, 8))

    buttons = tk.Frame(card, bg=PANEL)
    buttons.pack(fill="x", pady=(8, 0))

    submit_button = make_button(buttons, "SUBMIT ANSWER", submit_answer, PURPLE, 17)
    submit_button.pack(side="left")

    next_button = make_button(
        buttons,
        "SEE RESULTS  ➜" if current_question == TOTAL_QUESTIONS - 1 else "NEXT QUESTION  ➜",
        next_question, DARK_PURPLE, 17
    )
    next_button.pack(side="right")
    next_button.config(state="disabled", disabledforeground="#B6A8C6", bg="#D9CDE8")

    update_timer()


def update_timer():
    """Update the visible countdown once per second."""
    global time_left, timer_job

    if answered:
        return

    timer_label.config(
        text=f"TIME: {time_left}s",
        fg=RED if time_left <= 5 else "#FFE59A"
    )

    if time_left <= 0:
        time_up()
        return

    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    """Cancel the currently scheduled countdown callback."""
    global timer_job
    if timer_job is not None:
        try:
            root.after_cancel(timer_job)
        except tk.TclError:
            pass
        timer_job = None


def lock_choices():
    """Disable all answer choices after the question is completed."""
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    """Check the selected answer and show colored feedback."""
    global score, answered

    if answered:
        return

    choice = selected_answer.get()
    if not choice:
        messagebox.showwarning("No answer selected", "Please choose an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(
            text="✓  CORRECT! Great play! You earned 1 point.",
            fg=GREEN, bg=GREEN_BG, padx=12, pady=10
        )
    else:
        correct = get_choice_text(question, question["answer"])
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": correct
        })
        feedback_label.config(
            text=f"✗  NOT QUITE! The correct answer is {correct}.",
            fg=RED, bg=RED_BG, padx=12, pady=10
        )

    next_button.config(state="normal", bg=DARK_PURPLE, fg="white")


def time_up():
    """Mark the question incorrect when the countdown reaches zero."""
    global answered

    if answered:
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct = get_choice_text(question, question["answer"])
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time ran out)",
        "correct_answer": correct
    })

    feedback_label.config(
        text=f"TIME'S UP! The correct answer is {correct}.",
        fg=RED, bg=RED_BG, padx=12, pady=10
    )
    next_button.config(state="normal", bg=DARK_PURPLE, fg="white")


def next_question():
    """Move to the next question or display the final results."""
    global current_question
    if not answered:
        return

    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


def show_results():
    """Display the final score, percentage, high score, and answer review."""
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Amazing performance! You're a volleyball superstar!"
        message_color = GREEN
    elif percentage >= 70:
        message = "Great job! You know your volleyball basics."
        message_color = PURPLE
    elif percentage >= 50:
        message = "Nice effort! Keep practicing and you'll improve."
        message_color = GOLD
    else:
        message = "Good try! Review the game and come back stronger."
        message_color = RED

    header = tk.Frame(main_frame, bg=DARK_PURPLE, padx=22, pady=17)
    header.pack(fill="x", pady=(0, 13))

    tk.Label(
        header, text="MATCH COMPLETE!",
        font=("Segoe UI", 22, "bold"), bg=DARK_PURPLE, fg="white"
    ).pack(anchor="w")

    tk.Label(
        header, text=f"Well played, {player_name}!",
        font=("Segoe UI", 11), bg=DARK_PURPLE, fg="#E5D2FF"
    ).pack(anchor="w", pady=(3, 0))

    score_card = tk.Frame(main_frame, bg=PANEL, padx=18, pady=15,
                          highlightthickness=1, highlightbackground=LIGHT_PURPLE)
    score_card.pack(fill="x", pady=(0, 12))

    tk.Label(
        score_card, text=f"{score} / {total}",
        font=("Segoe UI", 29, "bold"), bg=PANEL, fg=DARK_PURPLE
    ).pack()

    tk.Label(
        score_card, text=f"FINAL SCORE  •  {percentage:.0f}%",
        font=("Segoe UI", 11, "bold"), bg=PANEL, fg=MUTED
    ).pack(pady=(0, 6))

    tk.Label(
        score_card, text=message, font=("Segoe UI", 11, "bold"),
        bg=PANEL, fg=message_color, wraplength=750
    ).pack()

    record_text = "★ NEW PERSONAL BEST!" if new_record else f"PERSONAL BEST: {get_high_score()} / {total}"
    tk.Label(
        score_card, text=record_text, font=("Segoe UI", 10, "bold"),
        bg=PANEL, fg=GOLD
    ).pack(pady=(7, 0))

    review_title = tk.Label(
        main_frame, text="ANSWER REVIEW",
        font=("Segoe UI", 12, "bold"), bg=BG, fg=DARK_PURPLE
    )
    review_title.pack(anchor="w", pady=(3, 6))

    review_frame = tk.Frame(main_frame, bg=PANEL)
    review_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")

    review_box = tk.Text(
        review_frame, height=8, wrap="word",
        font=("Segoe UI", 10), bg=PALE_PURPLE, fg=TEXT,
        relief="flat", padx=12, pady=10,
        yscrollcommand=scrollbar.set
    )
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "PERFECT GAME!\nYou answered all 10 questions correctly. Excellent work!")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")

    review_box.config(state="disabled")

    actions = tk.Frame(main_frame, bg=BG)
    actions.pack(pady=(12, 0))

    make_button(actions, "PLAY AGAIN", start_quiz, PURPLE, 16).pack(side="left", padx=7)
    make_button(actions, "EXIT", on_close, DARK_PURPLE, 12).pack(side="left", padx=7)


def on_close():
    """Stop the timer before closing the window."""
    stop_timer()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()
