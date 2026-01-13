import random
import tkinter as tk

kanji = ["日", "月", "火", "水"]
buttons = []
karten = kanji * 2
random.shuffle(karten)
time_limit = 60
time_left = time_limit
game_active = True

timer_id = None
buttons_locked = False

aufgedeckt = [False] * len(karten)
erste_auswahl = None



def game_win():
    global game_active
    game_active = False

    for button in buttons:
        button.configure(state="disabled")

    timer_label.configure(text="You Win")



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
    if karten[i1] == karten[i2]:
        global buttons_locked
        buttons_locked = False
    else:
        root.after(800, cover, i1, i2)

    if all(aufgedeckt):
        game_win()


def cover(i1, i2):
    buttons[i1].config(text="")
    buttons[i2].config(text="")
    aufgedeckt[i1] = False
    aufgedeckt[i2] = False
    buttons_locked = False

#daewd
äasd
# Buttons
root = tk.Tk()
root.title("Kanji Memory")

for i in range(len(karten)):
    btn = tk.Button(
        root,
        text="",
        width=6,
        height=3,
        font=("Arial", 20),
        command=lambda index=i: click_card(index)
    )
    btn.grid(row=(i // 4) + 1, column=i % 4, padx=5, pady=5)
    buttons.append(btn)

restart_button = tk.Button(
    root,
    text="Restart",
    font=("Arial", 12),
    command=lambda : restart_game()
)
restart_button.grid(row=0, column=4,padx=10)

def restart_game():
    global aufgedeckt, erste_auswahl, time_left, game_active, karten, timer_id

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

    timer_label.config(text=f"Time: {time_left}")

    timer_id = root.after(1000, update_timer)

# Timer
timer_label = tk.Label(root,
                       text=f"Time: {time_left}",
                       font=("Arial", 16),
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

    timer_label.config(text="Game Over")


root.after(1000, update_timer)          # Starts the timer
root.mainloop()