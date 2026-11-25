import json
from models import Character
from combat import Combat


class Game:
    def __init__(self, characters=None):
        self.characters = characters or []
        self.history = []
        self.turn_number = 0

    def living_characters(self):
        return [character for character in self.characters if character.is_alive]

    def start_battle(self):
        living = self.living_characters()
        if len(living) < 2:
            print("Для бою потрібно щонайменше два живих персонажі.")
            return

        order = sorted(living, key=lambda character: character.speed, reverse=True)
        self.turn_number += 1
        self.history.append(f"Крок {self.turn_number}: бій розпочато.")

        for attacker in order:
            if not attacker.is_alive:
                continue

            targets = [
                character for character in self.living_characters()
                if character is not attacker
            ]
            if not targets:
                break

            defender = min(targets, key=lambda character: character.health)
            damage = Combat.attack(attacker, defender)
            line = (
                f"{attacker.name} атакує {defender.name}: "
                f"{damage} шкоди. Здоров'я: {defender.health}/{defender.max_health}."
            )
            self.history.append(line)
            print(line)

        survivors = self.living_characters()
        if len(survivors) == 1:
            line = f"Переможець: {survivors[0].name}."
            self.history.append(line)
            print(line)
        elif not survivors:
            line = "Усі персонажі вибули з бою."
            self.history.append(line)
            print(line)

    def add_character(self, character):
        self.characters.append(character)
        self.history.append(f"Додано персонажа: {character.name}.")

    def add_character_from_input(self):
        try:
            name = input("Ім'я: ").strip()
            health = int(input("Здоров'я: "))
            damage = int(input("Шкода: "))
            armor = int(input("Броня: "))
            resist = float(input("Опір (від 0 до 1): "))
            speed = int(input("Швидкість: "))
            character = Character(name, health, damage, armor, resist, speed)
            self.add_character(character)
            print("Персонажа додано.")
        except ValueError as error:
            print(f"Не вдалося додати персонажа: {error}")

    def show_characters(self):
        if not self.characters:
            print("Персонажів поки немає.")
            return

        for character in self.characters:
            status = "живий" if character.is_alive else "вибув"
            print(
                f"{character.name}: HP {character.health}/{character.max_health}, "
                f"DMG {character.damage}, ARM {character.armor}, "
                f"RES {character.resist:.0%}, SPD {character.speed} ({status})"
            )

    def show_history(self):
        if not self.history:
            print("Історія поки порожня.")
            return

        for line in self.history:
            print(line)

    def save(self, filename="savegame.json"):
        data = {
            "characters": [character.to_dict() for character in self.characters],
            "history": self.history,
            "turn_number": self.turn_number
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Гру збережено.")

    @classmethod
    def load(cls, filename="savegame.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            game = cls([Character.from_dict(item) for item in data["characters"]])
            game.history = data.get("history", [])
            game.turn_number = data.get("turn_number", 0)
            print("Гру завантажено.")
            return game
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"Не вдалося завантажити гру: {error}")
            return cls()
