from game import Game
from models import Character


def create_game():
    player = Character("Мандрівник", 120, 24, 5, 0.10, 100)
    enemy = Character("Слизень", 80, 18, 3, 0.05, 80)
    return Game([player, enemy])


def main():
    game = create_game()

    while True:
        print("\n=== Текстова RPG ===")
        print("1. Почати бій")
        print("2. Додати персонажа")
        print("3. Показати персонажів")
        print("4. Зберегти гру")
        print("5. Завантажити гру")
        print("6. Історія бою")
        print("0. Вийти")

        choice = input("Вибір: ").strip()

        if choice == "1":
            game.start_battle()
        elif choice == "2":
            game.add_character_from_input()
        elif choice == "3":
            game.show_characters()
        elif choice == "4":
            game.save()
        elif choice == "5":
            game = Game.load()
        elif choice == "6":
            game.show_history()
        elif choice == "0":
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
