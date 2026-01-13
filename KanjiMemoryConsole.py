import random

kanji = ["日", "月", "火", "水"]
karten = kanji * 2
aufgedeckt = [False] * len(karten)

random.shuffle(karten)

def show_playfield():
    for i in range(len(karten)):
        if aufgedeckt[i]:
            print(f"{karten[i]} ", end="")
        else:
            print(f"{i} ", end="")
    print()  # Zeilenumbruch

show_playfield()


# Input Player
while not all(aufgedeckt):
    show_playfield()
    pos1 = int(input("Erste Karte wählen: "))
    pos2 = int(input("Zweite Karte wählen: "))

    aufgedeckt[pos1] = True
    aufgedeckt[pos2] = True

    show_playfield()

    if karten[pos1] == karten[pos2]:
        print("Correct")
    else:
        print("Incorrect")
        aufgedeckt[pos1] = False
        aufgedeckt[pos2] = False

print("Win")