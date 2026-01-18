import random
import tkinter as tk
import math
import pygame


class MemoryGame:
    def __init__(self, root, kanji_list):
        self.root = root
        pygame.mixer.init()
        self.kanji_list = kanji_list

        # Game state
        self.buttons = []
        self.aufgedeckt = []
        self.erste_auswahl = None
        self.buttons_locked = False
        self.game_active = True
        self.timer_id = None

        # Circle
        self.time_limit = 0
        self.visual_time = 0.0
        self.arc_job = None

        # Colors
        self.BG_COLOR = "#1e1e1e"
        self.BTN_COLOR = "#2d2d2d"
        self.TEXT_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#00ffcc"
        self.WIN_COLOR = "#4caf50"
        self.LOSE_COLOR = "#f44336"

        # Sounds
        self.sounds = {
            "flip": pygame.mixer.Sound("sounds/flip.mp3"),
            "match": pygame.mixer.Sound("sounds/match.mp3"),
            "wrong": pygame.mixer.Sound("sounds/wrong.mp3"),
            "win": pygame.mixer.Sound("sounds/win.mp3"),
            "lose": pygame.mixer.Sound("sounds/lose.mp3"),
        }

        for s in self.sounds.values():
            s.set_volume(0.5)

        # Difficulties
        max_pairs = len(self.kanji_list)

        self.difficulties = {
            "Easy": {"pairs": min(6, max_pairs), "cols": 4, "time": 60},
            "Medium": {"pairs": min(10, max_pairs), "cols": 5, "time": 50},
            "Hard": {"pairs": min(16, max_pairs), "cols": 8, "time": 60},
        }
        # Modes
        self.modes = {
            "Kanji - Kanji" : "kk",
            "Kanji - Meaning" : "km",
            "Kanji - Kana" : "kkana"
        }
        self.current_mode = "kk"

        self.current_difficulty = "Medium"

        # Animation
        self.FLIP_STEPS = 6
        self.FLIP_DELAY = 25
        self.CARD_WIDTH = 5

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
        self.difficulty_menu.config(bg=self.BG_COLOR,
                                    fg=self.TEXT_COLOR,
                                    relief="flat",
                                    highlightthickness=0)
        self.difficulty_menu.grid(row=0, column=5, padx=10)

        # ---------- Timer Frame ----------
        self.timer_frame = tk.Frame(
            self.root,
            bg=self.BG_COLOR
        )
        self.timer_frame.grid(
            row=0,
            column=0,
            rowspan=20,
            padx=20,
            sticky="n"
        )

        self.timer_canvas = tk.Canvas(
            self.timer_frame,
            width=80,
            height=80,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.timer_canvas.pack(pady=(150, 10))

        self.timer_arc = self.timer_canvas.create_arc(
            5, 5, 75, 75,
            start=90,
            extent=360,
            style=tk.ARC,
            outline=self.ACCENT_COLOR,
            width=4
        )

        self.timer_label = tk.Label(
            self.timer_frame,
            text="Time",
            font=("Arial", 16, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        self.timer_label.pack(pady=(0, 20))


        # Modes
        self.mode_var = tk.StringVar(value="Kanji - Kanji")

        self.mode_menu = tk.OptionMenu(
            self.root,
            self.mode_var,
            *self.modes.keys(),
            command=self.change_mode
        )
        self.mode_menu.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR, relief="flat",highlightthickness=0)
        self.mode_menu.grid(row=0, column=6, padx=10)



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
            btn.grid(row=(i // cols) + 1,
                     column=(i % cols) + 1,
                     padx=8,
                     pady=8)
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

        self.flip_card(index, show=True)
        self.aufgedeckt[index] = True

        if self.erste_auswahl is None:
            self.erste_auswahl = index
        else:
            self.buttons_locked = True
            self.root.after(600, self.check_pair, self.erste_auswahl, index)
            self.erste_auswahl = None

    def check_pair(self, i1, i2):
        if self.karten[i1]["id"] != self.karten[i2]["id"]:
            self.sounds["wrong"].play()
            self.flip_card(i1, show=False)
            self.flip_card(i2, show=False)
            self.aufgedeckt[i1] = self.aufgedeckt[i2] = False
        else:
            self.sounds["match"].play()
        self.buttons_locked = False

        if all(self.aufgedeckt):
            self.game_win()

    def game_win(self):
        self.game_active = False
        self.sounds["win"].play()
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="You Win!", fg=self.WIN_COLOR)

    def game_lose(self):
        self.game_active = False
        self.sounds["lose"].play()
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.timer_label.config(text="Time's up!", fg=self.LOSE_COLOR)

    def generate_cards(self, pairs):
        pairs = min(pairs, len(self.kanji_list))

        selected = random.sample(self.kanji_list, pairs)
        cards = []

        for idx, entry in enumerate(selected):
            if self.current_mode == "kk":
                cards.append({"id": idx, "text": entry["kanji"]})
                cards.append({"id": idx, "text": entry["kanji"]})
            elif self.current_mode == "km":
                cards.append({"id": idx, "text": entry["kanji"]})
                cards.append({"id": idx, "text": entry["meaning"]})
            elif self.current_mode == "kkana":
                cards.append({"id": idx, "text": entry["kanji"]})
                cards.append({"id": idx, "text": entry["kana"]})

        random.shuffle(cards)
        return cards


    # ---------- Timer ----------
    def start_timer(self):
        self.time_left = self.time_limit
        self.animate_timer_arc()
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

        if self.arc_job:
            self.root.after_cancel(self.arc_job)

        settings = self.difficulties[self.current_difficulty]
        self.time_limit = settings["time"]
        self.visual_time = float(self.time_limit)
        self.game_active = True
        self.buttons_locked = False
        self.erste_auswahl = None

        self.timer_canvas.itemconfig(
            self.timer_arc,
            extent=360,
            outline=self.ACCENT_COLOR
        )

        if full_reset:
            for btn in self.buttons:
                btn.destroy()

            pairs = settings["pairs"]
            cols = settings["cols"]

            self.karten = self.generate_cards(pairs)
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

    def change_mode(self, mode):
        self.current_mode = self.modes[mode]
        self.restart_game(full_reset=True)


# ---------- Animation ----------
    def flip_card(self, index, show=True, step=0):
        btn = self.buttons[index]

        if step == 0 and show:
            self.sounds["flip"].play()

        if step < self.FLIP_STEPS:
            width = self.CARD_WIDTH - step
            btn.config(width=max(1, width))
            self.root.after(
                self.FLIP_DELAY,
                self.flip_card,
                index,
                show,
                step + 1
            )

        elif step == self.FLIP_STEPS:
            btn.config(text=self.karten[index]["text"] if show else "")

            self.root.after(
                self.FLIP_DELAY,
                self.flip_card,
                index,
                show,
                step + 1
            )
        else:
            width = step - self.FLIP_STEPS
            btn.config(width=min(self.CARD_WIDTH, width))

            if width < self.CARD_WIDTH:
                self.root.after(
                    self.FLIP_DELAY,
                    self.flip_card,
                    index,
                    show,
                    step + 1
                )

# ---------- Animation ----------
    def animate_timer_arc(self):
        if not self.game_active:
            return

        self.visual_time -= 0.03

        if self.visual_time <= 0:
            self.visual_time = 0

        extent = (self.visual_time / self.time_limit) * 360
        self.timer_canvas.itemconfig(self.timer_arc, extent=extent)

        # Warning Color
        if self.visual_time <= self.time_limit * 0.25:
            self.timer_canvas.itemconfig(self.timer_arc, outline=self.LOSE_COLOR)

        self.arc_job = self.root.after(30, self.animate_timer_arc)

# ---------- Main ----------
if __name__ == "__main__":
    kanji_data = [
        {"kanji": "日", "kana": "にち", "meaning": "Sonne / Tag"},
        {"kanji": "月", "kana": "つき", "meaning": "Mond"},
        {"kanji": "火", "kana": "ひ", "meaning": "Feuer"},
        {"kanji": "水", "kana": "みず", "meaning": "Wasser"},
        {"kanji": "木", "kana": "き", "meaning": "Baum"},
        {"kanji": "金", "kana": "かね", "meaning": "Gold / Geld"},
        {"kanji": "土", "kana": "つち", "meaning": "Erde / Boden"},
        {"kanji": "山", "kana": "やま", "meaning": "Berg"},
        {"kanji": "川", "kana": "かわ", "meaning": "Fluss"},
        {"kanji": "田", "kana": "た", "meaning": "Reisfeld"},
        {"kanji": "人", "kana": "ひと", "meaning": "Person / Mensch"},
        {"kanji": "口", "kana": "くち", "meaning": "Mund"},
        {"kanji": "目", "kana": "め", "meaning": "Auge"},
        {"kanji": "耳", "kana": "みみ", "meaning": "Ohr"},
        {"kanji": "手", "kana": "て", "meaning": "Hand"},
        {"kanji": "足", "kana": "あし", "meaning": "Bein / Fuß"},
        {"kanji": "心", "kana": "こころ", "meaning": "Herz / Geist"},
        {"kanji": "力", "kana": "ちから", "meaning": "Kraft / Stärke"},
        {"kanji": "気", "kana": "き", "meaning": "Geist / Stimmung / Energie"},
        {"kanji": "白", "kana": "しろ", "meaning": "Weiß"},
        {"kanji": "黒", "kana": "くろ", "meaning": "Schwarz"},
        {"kanji": "赤", "kana": "あか", "meaning": "Rot"},
        {"kanji": "青", "kana": "あお", "meaning": "Blau"},
        {"kanji": "学", "kana": "がく", "meaning": "lernen / Schule"},
        {"kanji": "生", "kana": "せい", "meaning": "Leben / geboren"},
        {"kanji": "先", "kana": "せん", "meaning": "Zuvor / Lehrer"},
        {"kanji": "年", "kana": "ねん", "meaning": "Jahr"},
        {"kanji": "天", "kana": "てん", "meaning": "Himmel"},
        {"kanji": "車", "kana": "くるま", "meaning": "Auto / Wagen"},
        {"kanji": "門", "kana": "もん", "meaning": "Tor / Eingang"},
        {"kanji": "雨", "kana": "あめ", "meaning": "Regen"},
        {"kanji": "花", "kana": "はな", "meaning": "Blume"},
        {"kanji": "草", "kana": "くさ", "meaning": "Gras / Pflanze"},
        {"kanji": "魚", "kana": "さかな", "meaning": "Fisch"},
        {"kanji": "鳥", "kana": "とり", "meaning": "Vogel"},
        {"kanji": "犬", "kana": "いぬ", "meaning": "Hund"},
        {"kanji": "猫", "kana": "ねこ", "meaning": "Katze"},
        {"kanji": "時", "kana": "とき", "meaning": "Zeit / Stunde"},
        {"kanji": "分", "kana": "ふん", "meaning": "Minute / Teil"},
    ]

    root = tk.Tk()
    MemoryGame(root, kanji_data)
    root.mainloop()
