# pokeapi.py


import json
import urllib.request
import urllib.parse
import urllib.error

POKEAPIBASEURL = 'https://pokeapi.co/api/v2/pokemon/'
NUMPOKEMONURL = 'https://pokeapi.co/api/v2/pokemon?limit=2000'
MOVEAPIURL = 'https://pokeapi.co/api/v2/move/'


class pokeAPI:
    #I will later have to make these functions work fot the other pokemon json
    def __init__(self, pokemon_name, path, is_pokemon=True):
        print('using api')
        self.start_url = self._build_url(pokemon_name, is_pokemon)
        json_object = self._get_json(path)

    def _build_url(self, name, is_pokemon) -> str:
        """Create a url for the specific pokemon to use for API"""
        if is_pokemon:
            return (POKEAPIBASEURL + name)
        else:
            return (MOVEAPIURL + name)

    def _get_json(self, path) -> json:
        """Get the json object for a pokemon from the API (basically a list of list that has all the data we need)"""
        response = None
        try:
            #The 'Code Club' header is required or a 403 error occurs
            request = urllib.request.Request(self.start_url, headers={'User-Agent': 'Code Club'})
            response = urllib.request.urlopen(request)
            self.json_object = json.loads(response.read().decode(encoding='UTF-8'))
        except urllib.error.HTTPError:
            print('HTTP Error 404: Not Found')
            print(f'Tried to access {self.start_url}')
        finally:
            if response:
                response.close()
        self._make_file(path, self.json_object)
        return self.json_object
    
    def _make_file(self, path, contents) -> None:
        """Create a file at the objects path with the json object as contents"""
        with open(path, 'w') as file:
            file.write(json.dumps(contents))

    def get_stats(self) -> list[str]:
        """Return a list of stats summarizing the stat names and their values"""
        stats_dict = {}
        for stat in self.json_object['stats']:
            stats_dict[stat['stat']['name']] = stat['base_stat']
        return stats_dict

    def get_types(self) -> str:
        """Return a string naming the type of the pokemon"""
        json_types = self.json_object['types']
        if len(json_types) > 1 :
            type_list = []
            for i in json_types:
                type_list.append(i['type']['name'])
            type_output = '/'.join(type_list)
        else:
            type_output = json_types[0]['type']['name']
        return type_output

    def get_moves(self) -> list:
        """Return a list of moves that a pokemon can do"""
        return [move['move']['name'] for move in self.json_object['moves']]

    def get_move_info(self) -> tuple:
        """Get a tuple of damage class, accuracy, damage, and type"""
        accuracy = self.json_object['accuracy'] if self.json_object['accuracy'] else 100
        damage_class = self.json_object['damage_class']['name']
        power = self.json_object['power'] if self.json_object['power'] else 0
        move_type = self.json_object['type']['name']
        return accuracy, damage_class, power, move_type

class pokeFile:
    def __init__(self, pokemon_name, path):
        self.name = pokemon_name
        self.path = path
        json_object = self._get_json(path)
        
    def _get_json(self, path) -> json:
        """Parses the json form a pokemon's file"""
        with open(path, 'r') as file:
            json_text = file.read()
            self.json_object = json.loads(json_text)
        return self.json_object
    
    def get_stats(self) -> dict:
        """Return a list of stats summarizing the stat nmaes and their values"""
        stats_dict = {}
        for stat in self.json_object['stats']:
            stats_dict[stat['stat']['name']] = stat['base_stat']
        return stats_dict

    def get_types(self) -> str:
        """Return a string naming the type of the pokemon"""
        json_types = self.json_object['types']
        if len(json_types) > 1 :
            type_list = []
            for i in json_types:
                type_list.append(i['type']['name'])
            type_output = '/'.join(type_list)
        else:
            type_output = json_types[0]['type']['name']
        return type_output

    def get_moves(self) -> list:
        """Return a list of moves that a pokemon can do"""
        return [move['move']['name'] for move in self.json_object['moves']]

    def get_move_info(self) -> tuple:
        """Get a tuple of damage class, accuracy, damage, and type"""
        accuracy = self.json_object['accuracy'] if self.json_object['accuracy'] else 100
        damage_class = self.json_object['damage_class']['name']
        power = self.json_object['power'] if self.json_object['power'] else 0
        move_type = self.json_object['type']['name']
        return accuracy, damage_class, power, move_type


class NumPokemonHandler:
    def __init__(self):
        self.stats_dict = {}
        self.contents_url = NUMPOKEMONURL
        self.table_of_contents = self._get_json(self.contents_url)


    def _get_json(self, url) -> json:
        """Get the json object from a given URL"""
        response = None
        try:
            # The 'Code Club' header is required or a 403 error occurs
            request = urllib.request.Request(url, headers={'User-Agent': 'Code Club'})
            response = urllib.request.urlopen(request)
            json_object = json.loads(response.read().decode(encoding='UTF-8'))
        finally:
            if response:
                response.close()
        return json_object

    def get_contents(self) -> list:
        """Return a list of the pokemon names that need to be referenced"""
        return [pokemon['name'] for pokemon in self.table_of_contents['results']]

