from dataclasses import dataclass


@dataclass
class Character:
    name: str
    health: int
    damage: int
    armor: int
    resist: float
    speed: int

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Ім'я персонажа не може бути порожнім.")
        if min(self.health, self.damage, self.armor, self.speed) < 0:
            raise ValueError("Характеристики не можуть бути від'ємними.")
        if not 0 <= self.resist <= 1:
            raise ValueError("Опір має бути від 0 до 1.")
        self.max_health = self.health

    @property
    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def restore(self):
        self.health = self.max_health

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "damage": self.damage,
            "armor": self.armor,
            "resist": self.resist,
            "speed": self.speed,
            "max_health": self.max_health
        }

    @classmethod
    def from_dict(cls, data):
        character = cls(
            data["name"],
            data["health"],
            data["damage"],
            data["armor"],
            data["resist"],
            data["speed"]
        )
        character.max_health = data.get("max_health", character.health)
        return character
