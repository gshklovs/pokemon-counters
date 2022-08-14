# pokemon-counters
This is an application that gives the optimal counters to use agaisnt a given pokemon in descending order.
pokemon.py contains most of the main logic with type and stat advantantage calculations in calc.py.
I parsed json from the pokeapi in pokeapi.py and cached it until changes are made. 
A list of Pokemon are returned in descending order of viability index. 
Viability index is calculated through this formula:
VIndex = (Sum of Stats + Power of Strongest Move ) * Type Advantage / Opponents Type advantage.
The strength of the strongest move is determined by the SP-Attack or Attack stat (depending on the type of move) and the move's power and accuracy.
Thanks for checking out my project!
