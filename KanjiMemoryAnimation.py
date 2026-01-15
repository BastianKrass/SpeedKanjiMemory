import random
import tkinter as tk
import math


class MemoryGame:
    def __init__(self, root, kanji_list):
        self.root = root
        self.kanji_list = kanji_list

        # Game state
        self.buttons = []
        self.aufgedeckt = []
        self.erste_auswahl = None
        self.buttons_locked = False
        self.game_active = True
        self.timer_id = None

        # Colors
        self.BG_COLOR = "#1e1e1e"
        self.BTN_COLOR = "#2d2d2d"
        self.TEXT_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#00ffcc"
        self.WIN_COLOR = "#4caf50"
        self.LOSE_COLOR = "#f44336"

        # Difficulties
        self.difficulties = {
            "Easy": {"pairs": 6, "cols": 4, "time": 60},
            "Medium": {"pairs": 10, "cols": 5, "time": 50},
            "Hard": {"pairs": 16, "cols": 8, "time": 40},
        }
        self.current_difficulty = "Medium"

        self.setup_gui()
        self.restart_game(full_reset=True)

    # ---------- GUI ----------
    def setup_gui(self):
        self.root.title("Kanji Memory Game")
        self.root.configure(bg=self.BG_COLOR)

        self.timer_label = tk.Label(
            self.root,
            font=("Arial", 16),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        self.timer_label.grid(row=0, column=0, columnspan=4, pady=10)

        self.restart_button = tk.Button(
            self.root,
            text="Restart",
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            relief="flat",
            command=self.restart_game
        )
        self.restart_button.grid(row=0, column=4, padx=10)

        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        self.difficulty_menu = tk.OptionMenu(
            self.root,
            self.difficulty_var,
            *self.difficulties.keys(),
            command=self.change_difficulty
        )
        self.difficulty_menu.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR, relief="flat")
        self.difficulty_menu.grid(row=0, column=5, padx=10)

    # ---------- Cards ----------
    def create_cards(self, cols):
        self.buttons.clear()

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
                command=lambda index=i: self.click_card(index)
            )
            btn.grid(row=(i // cols) + 1, column=i % cols, padx=8, pady=8)
            self.buttons.append(btn)

        for c in range(cols):
            self.root.grid_columnconfigure(c, weight=1)
        for r in range(rows + 1):
            self.root.grid_rowconfigure(r, weight=1)

    # ---------- Game Logic ----------
    def click_card(self, index):
        if not self.game_active or self.buttons_locked:
            return
        if self.aufgedeckt[index]:
            return

        self.buttons[index].config(text=self.karten[index])
        self.aufgedeckt[index] = True

        if self.erste_auswahl is None:
            self.erste_auswahl = index
        else:
            self.buttons_locked = True
            self.root.after(600, self.check_pair, self.erste_auswahl, index)
            self.erste_auswahl = None

    def check_pair(self, i1, i2):
        if self.karten[i1] != self.karten[i2]:
            self.buttons[i1].config(text="")
            self.buttons[i2].config(text="")
            self.aufgedeckt[i1] = self.aufgedeckt[i2] = False

        self.buttons_locked = False

        if all(self.aufgedeckt):
            self.game_win()

    def game_win(self):
        self.game_active = False
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="You Win!", fg=self.WIN_COLOR)

    def game_lose(self):
        self.game_active = False
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="Time's up!", fg=self.LOSE_COLOR)

    # ---------- Timer ----------
    def start_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
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

    # ---------- Restart ----------
    def restart_game(self, full_reset=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        settings = self.difficulties[self.current_difficulty]
        self.time_left = settings["time"]
        self.game_active = True
        self.buttons_locked = False
        self.erste_auswahl = None

        if full_reset:
            for btn in self.buttons:
                btn.destroy()

            pairs = settings["pairs"]
            cols = settings["cols"]

            selected = random.sample(self.kanji_list, pairs)
            self.karten = selected * 2
            random.shuffle(self.karten)
            self.aufgedeckt = [False] * len(self.karten)

            self.create_cards(cols)
        else:
            random.shuffle(self.karten)
            self.aufgedeckt = [False] * len(self.karten)
            for btn in self.buttons:
                btn.config(text="", state=tk.NORMAL)

        self.start_timer()

    # ---------- Difficulty ----------
    def change_difficulty(self, level):
        self.current_difficulty = level
        self.restart_game(full_reset=True)


# ---------- Main ----------
if __name__ == "__main__":
    kanji_list = [
        "日", "月", "火", "水",
        "木", "金", "土",
        "山", "川", "田",
        "人", "口", "目",
        "手", "足", "心"
    ]

    root = tk.Tk()
    MemoryGame(root, kanji_list)
    root.mainloop()
