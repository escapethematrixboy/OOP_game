import random

class Character:
    def __init__(self, name, health, secondary_resource):
        self.name = name
        self._health = health
        self.secondary_resource = secondary_resource
        self.abilities = []

    def is_alive(self):
        return self._health > 0

    def take_damage(self, damage):
        self._health -= damage
        print(f"{self.name} took {damage} damage. Remaining health: {self._health}")

    def use_ability(self, ability, target):
        if self.is_alive():
            if self.secondary_resource >= ability['cost']:
                self.secondary_resource -= ability['cost']
                print(f"{self.name} used {ability['name']} on {target.name}")
                target.take_damage(ability['damage'])
            else:
                print(f"{self.name} doesn't have enough resources to use {ability['name']}!")
        else:
            print(f"{self.name} is dead and can't use abilities.")

class PlayerCharacter(Character):
    def __init__(self, name, health, secondary_resource, job):
        super().__init__(name, health, secondary_resource)
        self.job = job
        self.abilities = self.create_abilities()

    def create_abilities(self):
        if self.job == 'Warrior':
            return [
                {'name': 'Slash', 'damage': 20, 'cost': 10},
                {'name': 'Shield Bash', 'damage': 15, 'cost': 5},
                {'name': 'Rage', 'damage': 30, 'cost': 20}
            ]
        elif self.job == 'Mage':
            return [
                {'name': 'Fireball', 'damage': 25, 'cost': 15},
                {'name': 'Ice Blast', 'damage': 20, 'cost': 10},
                {'name': 'Arcane Missile', 'damage': 35, 'cost': 25}
            ]
        else:
            return []

    def show_resources(self):
        print(f"\n{self.name}'s Health: {self._health}")
        print(f"{self.name}'s {self.secondary_resource_name()}: {self.secondary_resource}\n")

    def secondary_resource_name(self):
        return "Mana" if self.job == "Mage" else "Stamina"

class Enemy(Character):
    def __init__(self, name, health, secondary_resource):
        super().__init__(name, health, secondary_resource)
        self.abilities = [
            {'name': 'Bite', 'damage': 10, 'cost': 5},
            {'name': 'Claw', 'damage': 15, 'cost': 8},
            {'name': 'Roar', 'damage': 20, 'cost': 12}
        ]

    def choose_ability(self):
        return random.choice(self.abilities)

class GameState:
    def __init__(self, player):
        self.player = player
        self.score = 0

    def enemy_turn(self, enemy):
        if enemy.is_alive():
            ability = enemy.choose_ability()
            print(f"Enemy {enemy.name} used {ability['name']}!")
            enemy.use_ability(ability, self.player)
        else:
            print(f"Enemy {enemy.name} is dead.")

    def player_turn(self, enemy):
        print(f"It's {self.player.name}'s turn.")
        self.player.show_resources()  # Display player's resources here
        print("Choose an ability:")
        for i, ability in enumerate(self.player.abilities):
            print(f"{i + 1}. {ability['name']} (Cost: {ability['cost']}, Damage: {ability['damage']})")
        
        choice = int(input("Choose ability number: ")) - 1
        if 0 <= choice < len(self.player.abilities):
            self.player.use_ability(self.player.abilities[choice], enemy)
        else:
            print("Invalid choice!")

    def check_battle_status(self, enemy):
        if not enemy.is_alive():
            self.score += 1
            print(f"{enemy.name} is defeated! Score: {self.score}")
            return True
        elif not self.player.is_alive():
            print(f"{self.player.name} is dead. Game Over.")
            return False
        return True

def main():
    player_name = input("Enter your character's name: ")
    player_job = input("Choose your class (Warrior/Mage): ")
    player = PlayerCharacter(player_name, health=100, secondary_resource=50, job=player_job)

    game_state = GameState(player)

    while player.is_alive():
        enemy = Enemy(name="Goblin", health=80, secondary_resource=30)
        print(f"A wild {enemy.name} appeared!")

        while enemy.is_alive() and player.is_alive():
            game_state.player_turn(enemy)
            if game_state.check_battle_status(enemy):
                game_state.enemy_turn(enemy)
                game_state.check_battle_status(enemy)
            else:
                break

    print(f"Game over! Your final score is: {game_state.score}")

if __name__ == "__main__":
    main()
