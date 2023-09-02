import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def is_known():
    to_learn.remove(current_card)
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_word()


def flip_card():
    english_word = current_card["English"]
    canvas.itemconfig(title_txt, text="English", fill="white")
    canvas.itemconfig(word_txt, text=english_word, fill="white")
    canvas.itemconfig(canvas_image, image=back_image)


def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_word = current_card["French"]
    canvas.itemconfig(title_txt, text="French", fill="black")
    canvas.itemconfig(word_txt, text=french_word, fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
back_image = PhotoImage(file="images/card_back.png")
front_image = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_image)
title_txt = canvas.create_text(400, 163, font=("Arial", 60, "italic"))
word_txt = canvas.create_text(400, 363, font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=next_word)
cross_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)
next_word()

window.mainloop()
