# pokemon.py
# the first time this program is run will take longer than all the rest
import pokeapi as api
from pathlib import Path
from calc import calculate_viability_index


def run(pokemon_name, list_len=10):
    """Get the top counters of a given pokemon"""
    #return ['sceptile-mega', 'exeggutor-alola', 'zekrom', 'ampharos-mega', 'eternatus-eternamax']
    #pokemon_name = get_pokemon_input()
    #pokemon_name = 'charmander'
    pokeapi_handler = get_handler(pokemon_name)
    my_stats_list = pokeapi_handler.get_stats()
    my_type = pokeapi_handler.get_types()
    list_of_names = get_pokemon_list()
    pokemon_to_viability_index = get_viability_list(list_of_names, my_type)
    return pokemon_to_viability_index[:list_len]


def get_pokemon_list() -> list:
    """Get a list of all pokemon names that I plan on parsing through"""
    pokemon_contents_handler = api.NumPokemonHandler()
    return pokemon_contents_handler.get_contents()


def get_viability_list(list_of_names: list, my_types: str) -> list:
    """Return a dictionary of pokemon to their viability index"""
    name_to_viability = {}
    for name in list_of_names:
        handler = get_handler(name)
        moves = get_moves_objects(handler)
        name_to_viability[name] = calculate_viability_index(handler, my_types, moves)
    return sorted(name_to_viability, key=lambda x: name_to_viability[x], reverse=True)


def get_pokemon_input() -> str:
    pokemon = input('Enter pokemon name or number\n>>> ')
    if pokemon.isdigit():
        pass
    else:
        pokemon = pokemon.lower()
    return pokemon


def get_handler(pokemon_name: str, path_name='cache', is_pokemon=True) -> 'pokemon_handler':
    """Get the correct type of handler depending on if a file already exists"""
    # check if a folder exists in the directory, if it doesn't, make a folder
    dir_path = Path(path_name)
    if not dir_path.exists():
        dir_path.mkdir(exist_ok = True)

    pokemon_path = dir_path / pokemon_name
    if pokemon_path.exists():
        try:
            return api.pokeFile(pokemon_name, pokemon_path)
        except urllib.error.URLError:
            return api.pokeAPI(pokemon_name, pokemon_path, is_pokemon=is_pokemon)
    else:
        return api.pokeAPI(pokemon_name, pokemon_path, is_pokemon=is_pokemon)


def get_moves_objects(handler) -> list:
    """Get a list of all the moves handler objects"""
    moves_list = handler.get_moves()
    move_objects = []
    for move_name in moves_list:
        move_handler = get_handler(move_name, path_name='move_cache', is_pokemon=False)
        move_objects.append(move_handler)
    return move_objects


if __name__ == "__main__":
    print(run('pikachu'))
