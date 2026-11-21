# VolleyVibe | Volleyball Challenge

**Name:** Johnell Arguelles Benedicto  
**Section:**  SE 3A
**Topic:** Volleyball Knowledge Quiz

## Features Completed

- [x] 10 multiple-choice questions
- [x] Four choices for every question (A to D)
- [x] Random question order
- [x] 15-second countdown timer for each question
- [x] Answer checking and time-out handling
- [x] Score and percentage calculation
- [x] Answer review for incorrect answers
- [x] High score saved in a text file
- [x] Restart button
- [x] Customized purple-themed interface
- [x] Player name entry
- [x] Progress bar and question indicator
- [x] Colored feedback for correct and incorrect answers

## How the Questions Are Stored and Shuffled

The 10 volleyball questions are stored in a Python list named `QUESTIONS`. Each question is represented by a dictionary containing the question, four answer choices, and the letter of the correct answer.

When the player starts or restarts the quiz, the program uses `random.sample()` to create a shuffled copy of the questions. This makes the question order different each time while keeping all 10 questions included in the quiz.

## How the Timer Works

The program uses a 15-second countdown for every question. The `update_timer()` function updates the time displayed on the screen every second using Tkinter's `root.after()` method.

When the player submits an answer, the `stop_timer()` function cancels the scheduled countdown so it will not continue running. If the timer reaches zero, the `time_up()` function automatically marks the question as incorrect and displays the correct answer. The player can no longer submit another answer for that question.

## How the Program Identifies the Correct Answer

Every question has an `answer` value in its dictionary, which contains the letter of the correct choice. When the player selects an answer and clicks the Submit Answer button, the program compares the selected letter with the stored correct answer.

If both letters match, the player receives one point and a green correct-answer message appears. If they do not match, the program displays red feedback and records the player's answer together with the correct answer for the review section.

The program also prevents double submission by checking whether the question has already been answered.

## How the Score and High Score Work

The player receives one point for every correct answer. After completing all 10 questions, the program calculates the percentage using the formula:

`(score / total questions) * 100`

The final results screen displays the player's score, percentage, and a performance message based on the result.

The high score is handled by two functions: `get_high_score()` and `save_high_score()`. The first reads the previous record from `volleyvibe_high_score.txt`. The second saves the new score only if it is higher than the previous record.

Since the text file is stored in the same directory as the Python program, the highest score remains available even after closing and reopening the application.

## Function Explanations

| Function | Purpose | Called When |
|---|---|---|
| `get_high_score()` | Reads the saved high score from the text file. | The start screen or results screen is displayed. |
| `save_high_score()` | Saves the new score if it is higher than the previous record. | The results screen is displayed. |
| `show_start_screen()` | Displays the welcome screen, player name entry, quiz information, and Start button. | The application is opened. |
| `start_quiz()` | Resets the quiz variables, shuffles the questions, and begins a new round. | Start or Play Again is clicked. |
| `show_question()` | Displays the current question, answer choices, timer, and progress bar. | A new question begins. |
| `update_timer()` | Updates the countdown and checks if time has run out. | A question is displayed and every second afterward. |
| `stop_timer()` | Cancels the active countdown. | An answer is submitted or the application closes. |
| `submit_answer()` | Checks the selected answer, updates the score, and displays feedback. | Submit Answer is clicked. |
| `time_up()` | Marks the question incorrect when the countdown reaches zero. | The timer expires. |
| `next_question()` | Moves to the next question or displays the final results. | Next Question is clicked. |
| `show_results()` | Displays the final score, percentage, performance message, and answer review. | All 10 questions are completed. |
| `on_close()` | Stops the timer and closes the application. | Exit is clicked or the window is closed. |

## Challenges I Faced

One of the challenges in developing this project was organizing the quiz functions so that the timer, answer checking, and score tracking would work properly together. I also had to make sure that the timer stopped after submitting an answer and that the player could not submit the same question more than once.

I addressed these by separating the program into different functions and using conditions to control the quiz flow. Another part was saving the high score using file handling so the record would remain even after closing the application.

Overall, this project helped me understand how Python Tkinter works, especially when creating graphical interfaces, handling user interactions, using functions, and managing data through text files.
