import json

with open('sheet.json') as f:
    data = json.load(f)['data']

    for mod_type in ['class', 'race', 'feat']:
        for pot_bonus in data['modifiers'][mod_type]:
            if pot_bonus['entityTypeId'] == 1472902489:
                data['stats'][pot_bonus['entityId']-1]['value'] += pot_bonus['value']

    s_str = data['stats'][0]['value']
    s_dex = data['stats'][1]['value']
    s_con = data['stats'][2]['value']
    s_int = data['stats'][3]['value']
    s_wis = data['stats'][4]['value']
    s_cha = data['stats'][5]['value']

    print(f"str: {s_str}")
    print(f"dex: {s_dex}")
    print(f"con: {s_con}")
    print(f"int: {s_int}")
    print(f"wis: {s_wis}")
    print(f"cha: {s_cha}")