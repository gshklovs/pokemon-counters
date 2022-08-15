# calc.py
TYPE_ADVANTAGE_STRING_RAW = '222221201222222222421124104222214241242221421224122222222111210224222224220424124421422222214212421422224222211122211124242241022222242222242212222224221112124224222221424114224122222244222411222122221144121141222122224202222241122122242422221222212202224242221114221422222222221222222420212222242222242211242122221122222442'
ROW_HEADERS = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy']


def _make_type_advantage_string() -> list:
    """Give back a list of strings that can be used to figure out the type advantage of a pokemon"""
    rows = []
    for i in range(18):
        row = []
        for j in range(18):
            index = (i * 18) + j
            row.append(TYPE_ADVANTAGE_STRING_RAW[index])
        rows.append(row)
    return rows


def _get_multiplier(attacker, defender, type_advantage_list) -> float:
    """Get the type advantage multiplier of 2 types"""
    row_index = ROW_HEADERS.index(attacker)
    col_index = ROW_HEADERS.index(defender)
    return float(type_advantage_list[row_index][col_index]) / 2


def calculate_type_advantage(user_type, opponent_type) -> int:
    """Using both the users and opponents types, returns a multiplier"""
    type_advantage_list = _make_type_advantage_string()
    advantage = 1
    if '/' in opponent_type:
        opponent_type = opponent_type.split('/')
        for opp_element in opponent_type:
            advantage *= calculate_type_advantage(user_type, opp_element)
    else:
        if '/' in user_type:
            user_type = user_type.split('/')
            for element in user_type:
                advantage *= _get_multiplier(element, opponent_type, type_advantage_list)
        else:
            advantage = _get_multiplier(user_type, opponent_type, type_advantage_list)
    return advantage


def calculate_viability_index(handler, opponent_type: str, moves: list) -> float:
    """Calculate the viability index given a pokemon's handler"""
    try:
        stats = handler.get_stats()
        types = handler.get_types()

        if type(stats) == list:
            hp, attack, defense, sp_attack, sp_defense, speed = stats[0]['base_stat'], stats[1]['base_stat'], stats[2]['base_stat'], stats[3]['base_stat'], stats[4]['base_stat'], stats[5]['base_stat']
        else:
            attack = stats['attack']
            sp_attack = stats['special-attack']
            hp, defense, sp_defense, speed = stats['hp'], stats['defense'], stats['special-defense'], stats['speed']

        strongest_move_strength = get_strongest_move(moves, opponent_type, sp_attack, attack)
        sum_of_stats = hp + defense + sp_defense + speed
        type_advantage = 1 / calculate_type_advantage(opponent_type, types) if calculate_type_advantage(opponent_type, types) else .25
    except TypeError as e:
        print('unknown format used for:')
        print(handler.start_url)
        print(stats)
        print(e)
        exit()

    return sum_of_stats * type_advantage * strongest_move_strength
    # sum of stats
    # strongest move for i in moves: get strongest move
    # type advantage
    # sum of stats (excluding sp and physical attack) * type advantage * (strongest move * the stat of the type of attack it is)


def get_strongest_move(moves: list, opponent_type: str, sp_attack, attack) -> float:
    """Get the strongest move a pokemon has against the given opponent and its type"""
    "how can i make this more effecient, what if each pokemon object built its own moveset"
    move_strength_list = []
    for move in moves:
        accuracy, damage_class, power, move_type = move.get_move_info()
        if move_type == 'physical':
            attack_stat = attack
        else:
            attack_stat = sp_attack
        move_strength = power * (accuracy / 100) * calculate_type_advantage(move_type, opponent_type) * attack_stat
        move_strength_list.append(move_strength)
    return max(move_strength_list) if move_strength_list else 0


def test_program():
    assert calculate_type_advantage('normal', 'ghost') == 0
    assert calculate_type_advantage('electric', 'dragon') == .5
    assert calculate_type_advantage('dark', 'water') == 1
    assert calculate_type_advantage( 'fire/steel', 'water') == .25


if __name__ == '__main__':
    test_program()
