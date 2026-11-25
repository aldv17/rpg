class Combat:
    @staticmethod
    def calculate_damage(attacker, defender):
        damage_after_armor = max(0, attacker.damage - defender.armor)
        damage_after_resist = damage_after_armor * (1 - defender.resist)
        return max(0, round(damage_after_resist))

    @staticmethod
    def attack(attacker, defender):
        damage = Combat.calculate_damage(attacker, defender)
        defender.take_damage(damage)
        return damage
