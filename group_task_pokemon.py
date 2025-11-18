import requests  # Allows python to make HTTP requests
import json  # Converts API responses (text) into python dictionaries
import random  # Used for randomly selecting Pokemon
import time  # Used to create thinking animation for realism


# CHANGES MADE BY GROUP:
# - Added CPU "thinking" animation with dots (makes it feel more realistic)
# - Added strength rating system that calculates attack + defense
# - Added CPU personality comments based on Pokemon strength
# - Combined player selection and CPU selection into one complete game
# - Kept the battle system that compares total power and declares winner

def get_random_pokemon():
    # pick a random pokemon from the original 151
    pokemon_id = random.randint(1, 151)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    response = requests.get(url)
    return json.loads(response.text)


def get_pokemon_by_name(name):
    # get pokemon data by name
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None
    except:
        return None


def get_stats(pokemon_data):
    # pull out the battle stats
    stats = {}
    for stat in pokemon_data['stats']:
        stat_name = stat['stat']['name']
        stat_value = stat['base_stat']
        stats[stat_name] = stat_value
    return stats


# NEW: Get strength rating (attack + defense) for CPU personality
def get_strength_rating(pokemon_data):
    stats = get_stats(pokemon_data)
    return stats['attack'] + stats['defense']


def display_pokemon(pokemon_data, is_cpu=False):
    # show pokemon info
    name = pokemon_data['name'].capitalize()
    height = pokemon_data['height'] / 10
    weight = pokemon_data['weight'] / 10

    # get the main ability
    abilities = pokemon_data['abilities']
    main_ability = abilities[0]['ability']['name']

    # get pokemon type
    types = [t['type']['name'] for t in pokemon_data['types']]
    type_str = '/'.join(types).upper()

    print(f"\n{'=' * 40}")
    print(f"Name: {name}")
    print(f"Type: {type_str}")
    print(f"Height: {height}m")
    print(f"Weight: {weight}kg")
    print(f"Ability: {main_ability}")

    # show stats
    stats = get_stats(pokemon_data)
    print(f"\nStats:")
    print(f"  HP: {stats['hp']}")
    print(f"  Attack: {stats['attack']}")
    print(f"  Defense: {stats['defense']}")
    print(f"  Speed: {stats['speed']}")
    print(f"  Total Power: {sum(stats.values())}")

    # NEW: Show strength rating and CPU personality for CPU pokemon
    if is_cpu:
        strength = get_strength_rating(pokemon_data)
        print(f"\nCPU Strength Rating: {strength}")

        # CPU comments based on strength
        if strength > 120:
            print("CPU: This Pokémon is powerful! Prepare yourself.")
        elif strength > 80:
            print("CPU: Decent strength! Let's see how this goes.")
        else:
            print("CPU: Hmm… this one isn't very strong, but I'll battle anyway!")

    print(f"{'=' * 40}")


def battle(pokemon1_data, pokemon2_data):
    # battle logic
    p1_name = pokemon1_data['name'].capitalize()
    p2_name = pokemon2_data['name'].capitalize()

    p1_stats = get_stats(pokemon1_data)
    p2_stats = get_stats(pokemon2_data)

    p1_power = sum(p1_stats.values())
    p2_power = sum(p2_stats.values())

    print(f"\n{'*' * 40}")
    print(f"BATTLE: {p1_name} vs {p2_name}")
    print(f"{'*' * 40}")

    print(f"\n{p1_name} power level: {p1_power}")
    print(f"{p2_name} power level: {p2_power}")

    print("\nBattling...")
    time.sleep(1)  # pause for effect

    # simple battle - highest power wins
    if p1_power > p2_power:
        print(f"\n{p1_name} wins!")
        return p1_name
    elif p2_power > p1_power:
        print(f"\n{p2_name} wins!")
        return p2_name
    else:
        print("\nIt's a draw!")
        return "Draw"


def main():
    print("=" * 40)
    print("POKEMON BATTLE GAME")
    print("=" * 40)

    # player picks their pokemon
    print("\nChoose your pokemon (or type 'random' for random):")
    choice = input("> ").lower().strip()

    if choice == 'random':
        print("\nGetting random pokemon...")
        player_pokemon = get_random_pokemon()
    else:
        print(f"\nSearching for {choice}...")
        player_pokemon = get_pokemon_by_name(choice)

        if player_pokemon is None:
            print("Pokemon not found! Getting random pokemon instead...")
            player_pokemon = get_random_pokemon()

    # NEW: CPU thinking animation
    print("\nCPU is selecting their pokemon", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

    # cpu gets random pokemon
    cpu_pokemon = get_random_pokemon()

    # show both pokemon
    print("\n--- YOUR POKEMON ---")
    display_pokemon(player_pokemon, is_cpu=False)

    print("\n--- CPU POKEMON ---")
    display_pokemon(cpu_pokemon, is_cpu=True)

    input("\nPress Enter to battle...")

    # battle
    winner = battle(player_pokemon, cpu_pokemon)

    print("\n" + "=" * 40)
    if winner == player_pokemon['name'].capitalize():
        print("YOU WIN!")
    elif winner == cpu_pokemon['name'].capitalize():
        print("YOU LOSE!")
    else:
        print("TIE GAME!")
    print("=" * 40)


if __name__ == "__main__":
    main()

