import requests as r
import os
import msvcrt as m
from time import sleep

clear = lambda: os.system('cls')
       

class Pokemon:
    def __init__(self, name, abilities, weight, types, species) -> None:
        self.name = name
        self.abilities = abilities
        self.weight = weight
        self.types = types
        self.species = species
        
    def view(self):
        print('Name:', self.name.title())
        print('Abilities: ', end = "")
        print(", ".join(self.abilities).title())
        print("Weight:", self.weight)
        print("Types: ", ", ".join(self.types).title())
        print(f'Species: {self.species}')
        
    def desc_as_dict(self):
        return self.__dict__
    
    def report_name(self):
        print('Name:', self.name)
    
    def get_types(self):
        return self.types
        

class Pokedex:
    def __init__(self):
        self.pokemon = {}
        self.pokemon_by_type = {}
        self.pokemon_by_species = {}
        self.types = []
        self.species = []
        self.abilities = {}
        
    def add_pokemon(self, pokemon):
        self.pokemon[pokemon.name] = pokemon
        
    def listAll(self):
        for name, info in self.pokemon.items():
            print(f'{name}'.title(), f"({', '.join(info.types)})")
            
    def search(self, name):
        self.pokemon[name.lower()].view()
    
    def get_ability(self,name):
        if not self.pokemon.get(name):
            data = r.get(f"https://pokeapi.co/api/v2/ability/{name}")
            if data.status_code == 200:
                data = data.json()
                ability = {
                    "name": data['name'],
                    "effects": [effect["short_effect"] for effect in data['effect_entries'] if effect['language']['name'] == "en"],
                    "pokemon": [p['pokemon']['name'] for p in data['pokemon']]
                }
                self.abilities[name] = ability
            else:
                print('Error getting abilities')
            return ability
    
    def get_types(self) -> None:
        """Populates types list"""
        data = r.get(f'https://pokeapi.co/api/v2/type/')
        if data.status_code == 200:
            data = data.json()['results']
            self.types = [d['name'] for d in data]
        else:
            print('Error getting types')
        
    def print_types(self):
        print("' ,'.join([x for x in self.types])")
                    
    def print_types_species(self):
        for p in self.pokemon:
            print(p.name, "- ",p.species, "- ", ", ".join(p.types))
            
    def list_by_type(self):
        # for each poke 
        for pokemon in self.pokemon.values():
            # loop through types
            for this_type in pokemon.types:
                # set the value to a dict item, as a dictionary, appending the name                
                self.species_by_type.setdefault(this_type, []).append(pokemon.name)
        for k, v in self.species_by_type.items():
            print(f"{k}:".title(), f"{', '.join(v)}".title())
              
    def get_pokemon(self, name) -> Pokemon:
        """fetches pokemon, adds to dex, & returns obj"""
        # populate pokemon names from type if not already
        if not self.pokemon.get(name):
            type_data = r.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
            if type_data.status_code == 200:
                data = type_data.json()
                pokemon = Pokemon(
                    name=data['name'], 
                    abilities = [ability['ability']['name'] for ability in data['abilities']], 
                    weight = data['weight'], 
                    types = [t['type']['name'] for t in data['types']], 
                    species = data['species']['name'])
                self.add_pokemon(pokemon)
                return self.pokemon.get(name)
            else: 
                print('\nData not retrieved (name probably not found)')
                acknowledge()
                return None
        else:
            return self.get(name)

    def get_pokemon_by_type(self, type_name):
        # populate pokemon names from type if not already
        if not self.pokemon_by_type.get(type_name):
            type_data = r.get(f'https://pokeapi.co/api/v2/type/{type_name}')
            if type_data.status_code == 200:
                pokemon_from_type = type_data.json()['pokemon']
                self.pokemon_by_type[type_name] = sorted([pokemon['pokemon']['name'] for pokemon in pokemon_from_type])
            else: 
                print('Type data not retrieved')


# end pokedex
class Explorer:
    def __init__(self, pokedex) -> None:
        self.pokedex = pokedex
   
    def run(self):
        self.intro()
        self.main_menu()
        print("Exiting Pokemon Explorer...")
        sleep(2)

    def intro(self):
        clear()
        print("Welcome to the Pokemon Explorer. \nHere, you can search for pokemon and learn about their abilities. \n")
        acknowledge()
        
    def main_menu(self):
        clear()
        while True:
            clear()
            ans = input('\n[Search by name] or go to the [T]ype list... or [Q]uit: ').lower()
            if ans == 'q':
                break
            if ans == 't':
                self.search_by_type()
            if len(ans) > 1:
                pokemon = self.search_by_name(ans)
                if pokemon == 'Not Found':
                    print('Pokemon Not Found')
                    continue
                else: 
                    self.pokemon_menu(pokemon)
            else:
                print('What?')            
                
    def search_by_type(self):
        if len(self.pokedex.types) == 0:
            print('Getting types...')
            self.pokedex.get_types()        
        
        clear()
        print(' Select Type '.center(30, "-"))
        type_pick = select_from_list(self.pokedex.types)
        if not type_pick:
            return
        # populate pokemon names from type if not already
        self.pokedex.get_pokemon_by_type(type_pick)
        
        clear()
        print(f'Showing results for {type_pick}')
        print('Pick a pokemon'.center(30, '-'))
        pokemon_pick = select_from_list(self.pokedex.pokemon_by_type[type_pick])
        if not pokemon_pick:
            return
        
        pokemon = self.pokedex.get_pokemon(pokemon_pick)
        self.pokemon_menu(pokemon)
        
    def pokemon_menu(self, pokemon):
        """ takes pokemon object, shows attributes & option to view abilities"""
        while True:
            clear()
            pokemon.view()
            print('\n[D]isplay abilities   [R]eturn to Search Menu')
            ans = input().lower()        
            if ans == 'd':
                self.display_abilities(pokemon)
                acknowledge()
            if ans == 'r':
                break
            else: 
                print('What?')
          
    def search_by_name(self,name) -> str:
        if not self.pokedex.pokemon.get(name):            
            if not self.pokedex.get_pokemon(name): 
                return 'Not Found'
        return self.pokedex.pokemon[name]
    
    def display_abilities(self, pokemon):
        print()
        print(f' {pokemon.name.title()} Abilities'.center(30, '-'))
        for ability_name in pokemon.abilities:
            ability = self.pokedex.get_ability(ability_name)
            print(f"\n{ability['name']}".upper())
            for effect in ability['effects']:
                print(f"- {effect}")

class MainUI:
    def __init__(self) -> None:
        pass
        
    def mainMenu(self, pokedex):
        while True:
            clear()
            print("Hello, and welcome to the Pokemon Main Menu & Welcoming Center. \n\nDo you feel welcomed? Don't answer. There's no input mechanic for that.\n\n")
            print("You can do these things: \n")
            ans = input('[E]xplore Pokemon & Their Abilities \n[Q]uit \n\nEnter choice: ').lower()
            if ans == 'e':
                expl = Explorer(pokedex)
                expl.run()
            if ans == 'q':
                break
            else:
                print("What? I didn't understand that.")
        pokedex.print_types()
    
    def goodbye(self):
        clear()
        print("Well, it's been nice. Come back again soon!")
        sleep(3)
    
def acknowledge():    
    print('\nPress any key to continue... ')
    m.getch()

def select_from_list(this_list) -> str:
    print("")
    groupby4 = len(this_list) // 4
    for i in range(groupby4): 
        print(f"[{4*i+1}]".rjust(4), f"{this_list[4*i].title()}".ljust(15), end="  ")
        print(f"[{4*i+2}]".rjust(4), f"{this_list[4*i+1].title()}".ljust(15), end="  ")
        print(f"[{4*i+3}]".rjust(4), f"{this_list[4*i+2].title()}".ljust(15), end="  ")
        print(f"[{4*i+4}]".rjust(4), f"{this_list[4*i+3].title()}".ljust(15))
    leftby4 = len(this_list) % 4
    for i in range(leftby4): 
        print(f"[{4*groupby4 + i + 1}]".rjust(4), f"{this_list[4*groupby4 + i].title()}".ljust(15), end = "  ")
    print('')
    
    while True:
        pick_index = input("\nSelect by number (or [B]ack): ")
        if pick_index in ['b', 'B']:
            return
        else:
            try:
                pick_index = int(pick_index)
                if pick_index > len(this_list) or pick_index <= 0:
                    print("Your response wasn't a listed option.")
                    continue
                else:
                    pick_index -= 1
                    break
            except:
                print("Your response wasn't recognized")
                continue
            
    return this_list[pick_index]
 

def main():
    pokedex = Pokedex()
    ui = MainUI()
    ui.mainMenu(pokedex)
    ui.goodbye()
    
main()