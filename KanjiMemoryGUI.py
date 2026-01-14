import random
import tkinter as tk
import math

kanji = [
    "日", "月", "火", "水",
    "木", "金", "土",
    "山", "川", "田",
    "人", "口", "目",
    "手", "足", "心"
]
buttons = []
karten = kanji * 2



random.shuffle(karten)
time_limit = 20
time_left = time_limit
game_active = True

timer_id = None
buttons_locked = False

aufgedeckt = [False] * len(karten)
erste_auswahl = None

BG_COLOR = "#1e1e1e"
BTN_COLOR = "#2d2d2d"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#00ffcc"
WIN_COLOR = "#4caf50"
LOSE_COLOR = "#f44336"


def game_win():
    global game_active
    game_active = False

    for button in buttons:
        button.configure(state="disabled")

    timer_label.configure(text="You Win", fg=WIN_COLOR)



def click_card(index):
    global erste_auswahl, buttons_locked

    if not game_active or buttons_locked:
        return


    if aufgedeckt[index]:
        return

    buttons[index].config(text=karten[index])
    aufgedeckt[index] = True

    if erste_auswahl is None:
        erste_auswahl = index
    else:
        buttons_locked = True
        check_pair(erste_auswahl, index)
        erste_auswahl = None


def check_pair(i1, i2):
    global buttons_locked

    if karten[i1] == karten[i2]:
        buttons_locked = False
    else:
        root.after(800, cover, i1, i2)

    if all(aufgedeckt):
        game_win()


def cover(i1, i2):
    global buttons_locked

    buttons[i1].config(text="")
    buttons[i2].config(text="")
    aufgedeckt[i1] = False
    aufgedeckt[i2] = False

    buttons_locked = False

# GUI
root = tk.Tk()
root.title("Kanji Memory")

root.configure(bg=BG_COLOR)

# Buttons
for i in range(len(karten)):
    btn = tk.Button(
        root,
        text="",
        width=5,
        height=2,
        font=("Arial", 22, "bold"),
        bg=BTN_COLOR,
        fg=TEXT_COLOR,
        relief="flat",
        activebackground="#3a3a3a",
        activeforeground=TEXT_COLOR,
        command=lambda index=i: click_card(index)
    )
    cols = 8
    rows = math.ceil(len(karten) / cols)
    btn.grid(
        row=(i // cols) + 1,
        column=i % cols,
        padx = 8,
        pady = 8,
        sticky="nsew"
    )
    buttons.append(btn)

restart_button = tk.Button(
    root,
    text="Restart",
    font=("Arial", 12),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    activebackground="#3a3a3a",
    activeforeground=TEXT_COLOR,
    relief="flat",
    command=lambda : restart_game()
)
restart_button.grid(row=0, column=4,padx=10)



def restart_game():
    global aufgedeckt, erste_auswahl, time_left, game_active, karten, timer_id, buttons_locked
    buttons_locked = False

    if timer_id is not None:
        root.after_cancel(timer_id)

    # Gamestatus reset
    erste_auswahl = None
    game_active = True
    time_left = time_limit

    random.shuffle(karten)

    aufgedeckt = [False] * len(karten)

    for btn in buttons:
        btn.config(text="", state="normal")

    timer_label.config(text=f"Time: {time_left}", fg=ACCENT_COLOR)

    timer_id = root.after(1000, update_timer)


# Timer
timer_label = tk.Label(root,
                       text=f"Time: {time_left}",
                       font=("Arial", 16),
                       fg=ACCENT_COLOR,
                       bg=BG_COLOR,
                       )
timer_label.grid(row=0, column=0, columnspan=4, pady= 10)



def update_timer():
    global time_left, game_active, timer_id

    if not game_active:
        return

    time_left -= 1
    timer_label.config(text=f"Time: {time_left}")

    if time_left <= 0:
        game_active = False
        game_lose()
    else:
        timer_id = root.after(1000, update_timer)



def game_lose():
    for btn in buttons:
        btn.config(state="disabled")

    timer_label.config(text="Game Over", fg=LOSE_COLOR)


root.after(1000, update_timer)          # Starts the timer
root.mainloop()