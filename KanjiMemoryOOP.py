import random
import tkinter
import tkinter as tk
import math

class MemoryGame:
    def __init__(self, root, kanji_list, time_limit=60):
        # GUI & Game state
        self.root = root
        self.kanji_list = kanji_list
        self.time_limit = time_limit
        self.time_left = time_limit
        self.game_active = True
        self.buttons_locked = False
        self.aufgedeckt = []
        self.buttons = []
        self.erste_auswahl = None
        self.timer_id = None

        # Farben
        self.BG_COLOR = "#1e1e1e"
        self.BTN_COLOR = "#2d2d2d"
        self.TEXT_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#00ffcc"
        self.WIN_COLOR = "#4caf50"
        self.LOSE_COLOR = "#f44336"

        # Setup GUI
        self.setup_gui()
        self.start_timer()

    # Methoden
    def setup_gui(self):
        self.root.title("Kanji Memory Game")
        self.root.configure(background=self.BG_COLOR)

        # Prepare cards
        self.karten = self.kanji_list * 2
        random.shuffle(self.karten)
        self.aufgedeckt = [False] * len(self.karten)

        # Timer
        self.timer_label = tk.Label(
            self.root,
            text=f"Time: {self.time_left}",
            font=("Arial", 16),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR,
        )
        self.timer_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Restart Button
        self.restart_button = tk.Button(
            self.root,
            text="Restart",
            font=("Arial", 12),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            activebackground="#3a3a3a",
            activeforeground=self.TEXT_COLOR,
            relief="flat",
            command=self.restart_game
        )
        self.restart_button.grid(row=0, column=4, padx=10)

        # Create card buttons
        self.buttons = []
        cols = 8
        rows = math.ceil(len(self.karten) / cols)

        for i in range(len(self.karten)):
            btn = tk.Button(
                self.root,
                text="",
                width=5,
                height=2,
                font=("Arial", 22, "bold"),
                bg=self.BTN_COLOR,
                fg=self.TEXT_COLOR,
                relief="flat",
                activebackground="#3a3a3a",
                activeforeground=self.TEXT_COLOR,
                command=lambda index=i: self.click_card(index)
            )
            btn.grid(
                row=(i // cols) + 1,
                column=i % cols,
                padx=8,
                pady=8,
                sticky="nsew"
            )
            self.buttons.append(btn)
        for c in range(cols):
            self.root.grid_columnconfigure(c, weight=1)
        for r in range(rows + 1):
            self.root.grid_rowconfigure(r, weight=1)


# ---------------- Game Logic ----------------
    def click_card(self, index):
        if not self.game_active or self.buttons_locked:
            return

        if self.aufgedeckt[index]:
            return

        # Reveal card
        self.buttons[index].config(text=self.karten[index])
        self.aufgedeckt[index] = True

        if self.erste_auswahl is None:
            self.erste_auswahl = index
        else:
            self.buttons_locked = True
            self.check_pair(self.erste_auswahl, index)
            self.erste_auswahl = None

    def check_pair(self, i1, i2):
        if self.karten[i1] == self.karten[i2]:
            self.buttons_locked = False
        else:
            self.root.after(800, self.cover, i1, i2)


        if all(self.aufgedeckt):
            self.game_win()

    def cover(self, i1, i2):
        self.buttons[i1].config(text="")
        self.buttons[i2].config(text="")
        self.aufgedeckt[i1] = False
        self.aufgedeckt[i2] = False
        self.buttons_locked = False

    def game_win(self):
        self.game_active = False
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="You Win", fg=self.WIN_COLOR)

    def game_lose(self):
        self.game_active = False
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="You Lose", fg=self.LOSE_COLOR)


# ---------------- Timer ----------------
    def start_timer(self):
        self.timer_id = self.root.after(1000, self.update_timer)

    def update_timer(self):
        if not self.game_active:
            return
        self.time_left -= 1
        self.timer_label.config(text=f"Time: {self.time_left}")

        if self.time_left <= 0:
            self.game_lose()
        else:
            self.timer_id = self.root.after(1000, self.update_timer)


# ---------------- Restart ----------------
    def restart_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.time_left = self.time_limit
        self.game_active = True
        self.buttons_locked = False
        self.erste_auswahl = None

        random.shuffle(self.karten)
        self.aufgedeckt = [False] * len(self.karten)

        for btn in self.buttons:
            btn.config(text="",state="normal")

        self.timer_label.config(text=f"Time: {self.time_left}", fg=self.ACCENT_COLOR)
        self.start_timer()


# ---------------- Main ----------------
if __name__ == "__main__":
    kanji_list = [
        "日", "月", "火", "水",
        "木", "金", "土",
        "山", "川", "田",
        "人", "口", "目",
        "手", "足", "心"
    ]
    root = tk.Tk()
    game = MemoryGame(root, kanji_list, time_limit=60)
    root.mainloop()