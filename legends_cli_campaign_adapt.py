import random
import json
import os

SAVE_FILE = "kl_save.json"

class Game:
    def __init__(self):
        self.board_size = 9
        self.hero_pos = [0, 0]
        self.enemy_pos = [self.board_size - 1, self.board_size - 1]
        self.level = 1
        self.gold = 0
        self.lifelines = 3   # Start with 3 lifelines
        self.hero_power = True
        self.mimic_attempts = 3
        self.history = []
        self.load_progress()

    def save_progress(self):
        state = {
            "hero_pos": self.hero_pos,
            "enemy_pos": self.enemy_pos,
            "level": self.level,
            "gold": self.gold,
            "lifelines": self.lifelines,
            "hero_power": self.hero_power,
            "mimic_attempts": self.mimic_attempts,
            "history": self.history
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(state, f)

    def load_progress(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                state = json.load(f)
                self.hero_pos = state["hero_pos"]
                self.enemy_pos = state["enemy_pos"]
                self.level = state["level"]
                self.gold = state["gold"]
                self.lifelines = state["lifelines"]
                self.hero_power = state["hero_power"]
                self.mimic_attempts = state["mimic_attempts"]
                self.history = state["history"]

    def draw_board(self):
        for i in range(self.board_size):
            row = ""
            for j in range(self.board_size):
                if [i, j] == self.hero_pos:
                    row += " H "
                elif [i, j] == self.enemy_pos:
                    row += " E "
                else:
                    row += " . "
            print(row)
        print(f"Level: {self.level} | Gold: {self.gold} | Lifelines: {self.lifelines} | Power-Up: {self.hero_power}")

    def move_hero(self, move):
        if move == "W" and self.hero_pos[0] > 0:
            self.hero_pos[0] -= 1
        elif move == "S" and self.hero_pos[0] < self.board_size - 1:
            self.hero_pos[0] += 1
        elif move == "A" and self.hero_pos[1] > 0:
            self.hero_pos[1] -= 1
        elif move == "D" and self.hero_pos[1] < self.board_size - 1:
            self.hero_pos[1] += 1
        elif move == "L" and self.lifelines > 0:
            self.enemy_pos = [self.board_size - 1, self.board_size - 1]
            self.lifelines -= 1

    def move_enemy(self):
        hx, hy = self.hero_pos
        ex, ey = self.enemy_pos

        dx = hx - ex
        dy = hy - ey

        if self.level <= 3:
            move_choice = random.choice(["x", "y"])
        elif self.level <= 6:
            move_choice = "x" if abs(dx) > abs(dy) else "y"
        elif self.level <= 10:
            move_choice = "x" if abs(dx) >= abs(dy) else "y"
        else:
            # Adaptive mimic behavior
            if self.history and random.random() > 0.3:
                last_move = self.history[-1]
                move_choice = "x" if last_move in ["W", "S"] else "y"
            else:
                move_choice = "x" if abs(dx) >= abs(dy) else "y"

        if move_choice == "x":
            if dx > 0:
                ex += 1
            elif dx < 0:
                ex -= 1
        elif move_choice == "y":
            if dy > 0:
                ey += 1
            elif dy < 0:
                ey -= 1

        self.enemy_pos = [ex, ey]

    def play_level(self):
        self.hero_pos = [0, 0]
        self.enemy_pos = [self.board_size - 1, self.board_size - 1]

        while True:
            os.system("clear" if os.name != "nt" else "cls")
            self.draw_board()

            if self.hero_pos == self.enemy_pos:
                print("💀 You were caught!")
                self.lifelines = max(0, self.lifelines - 1)
                self.hero_power = True
                return False

            if self.hero_pos == [self.board_size - 1, self.board_size - 1]:
                print("🎉 Level cleared!")
                self.gold += 10
                return True

            move = input("Move (WASD, L for Lifeline, Q to quit): ").upper()
            if move == "Q":
                self.save_progress()
                print("Game saved. Come back soon!")
                exit()
            self.move_hero(move)
            self.history.append(move)
            self.move_enemy()

    def run(self):
        while self.level <= 15:
            print(f"🔥 Starting Level {self.level}")
            if self.play_level():
                # Lifeline regen every 4 levels
                if self.level % 4 == 0:
                    self.lifelines += 1
                    print("✨ You gained +1 Lifeline for surviving 4 levels!")

                self.level += 1

                # Offer lifeline purchase
                if self.gold >= 50:
                    buy = input("Buy lifeline for 50 gold? (y/n): ").lower()
                    if buy == "y" and self.gold >= 50:
                        self.lifelines += 1
                        self.gold -= 50
            else:
                print("Try again from this level!")
                self.save_progress()
                return

        self.boss_fight()

    def boss_fight(self):
        print("🐉 Final Boss: The Mimic Beast Appears!")
        while self.mimic_attempts > 0:
            self.hero_pos = [0, 0]
            self.enemy_pos = [self.board_size - 1, self.board_size - 1]
            while True:
                os.system("clear" if os.name != "nt" else "cls")
                self.draw_board()

                if self.hero_pos == self.enemy_pos:
                    print("💀 The Mimic Beast devoured you!")
                    self.mimic_attempts -= 1
                    break

                if self.hero_pos == [self.board_size - 1, self.board_size - 1]:
                    print("🎉 You defeated the Mimic Beast and saved the Kingdom!")
                    return

                move = input("Move (WASD, P for Power-Up, Q to quit): ").upper()
                if move == "Q":
                    self.save_progress()
                    print("Game saved. Come back soon!")
                    exit()
                if move == "P" and self.hero_power:
                    print("⚡ Hero Power Activated!")
                    self.hero_power = False
                    continue
                self.move_hero(move)
                self.history.append(move)
                self.move_enemy()

        print("💀 All attempts failed. Restarting your journey...")
        self.level = 1
        self.save_progress()

if __name__ == "__main__":
    game = Game()
    game.run()
