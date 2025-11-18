import requests  # Allows python to make HTTP requests
import json      # Converts API responses (text) into python dictionaries
import random    # I used it so the CPU can be randomly select a Pokemon
import time      # I used to create thinking animation for realism

 ## User story- As a CPU, I want to automatically select a random Pokemon
 ## So that the game feels fair and unpredictable.


# Function to fetch a random Pokémon

def get_random_cpu_pokemon():
    random_id = random.randint(1, 151)  # Pokémon provides data based on this ID number
    url = f'https://pokeapi.co/api/v2/pokemon/{random_id}/'

    # send a request to the PokeAPI to get information about this Pokemon
    response = requests.get(url)

    # It converts the API text response into a Python dictionaries

    pokemon_data = json.loads(response.text)
    # return the data, so the CPU can use it later
    return pokemon_data


# NEW: Simple CPU strength score (attack + defense)
def get_cpu_strength(pokemon):
    attack = pokemon['stats'][1]['base_stat']
    defense = pokemon['stats'][2]['base_stat']
    return attack + defense


# Function to display CPU Pokémon information
def display_cpu_pokemon(pokemon_data):
    name = pokemon_data['name'].capitalize()
    height = pokemon_data['height'] / 10
    weight = pokemon_data['weight'] / 10
    ability = pokemon_data['abilities'][0]['ability']['name']
    type_list = [t['type']['name'] for t in pokemon_data['types']]
    pokemon_type = "/".join(type_list)

    print("\nCPU Pokémon Selected:")
    print(f"Name: {name}")
    print(f"Type: {pokemon_type}")
    print(f"Height: {height} m")
    print(f"Weight: {weight} kg")
    print(f"Ability: {ability}")

    strength = get_cpu_strength(pokemon_data)
    print(f"CPU Strength Rating: {strength}")

    # CPU strategy comment
    if strength > 120:
        print("CPU: This Pokémon is powerful! Prepare yourself.")
    elif strength > 80:
        print("CPU: Decent strength! Let's see how this goes.")
    else:
        print("CPU: Hmm… this one isn’t very strong, but I'll battle anyway!")


# Main function demonstrating CPU selection
# It brings all functions together.

def main():
    print("CPU is selecting a random Pokémon...")

    # It shows the CPU thinking animation.
    print("CPU is thinking", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")
    print()

    cpu_pokemon = get_random_cpu_pokemon()  # CPU gets random Pokémon

    display_cpu_pokemon(cpu_pokemon)        # Show CPU Pokémon details


# Run the program
if __name__ == "__main__":
    main()

