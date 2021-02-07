import urllib.request, json 

def total_to_bonus(val):
    bonus = (val - 10) / 2
    if bonus < 0:
        bonus -= 0.5
    return int(bonus)

skills = {
    'acrobatics':'dex',
    'animal_handling':'wis',
    'arcana':'int',
    'athletics':'str',
    'deception':'cha',
    'history':'int',
    'insight':'wis',
    'intimidation':'cha',
    'investigation':'int',
    'medicine':'wis',
    'nature':'int',
    'perception':'wis',
    'performance':'cha',
    'persuasion':'cha',
    'religion':'int',
    'sleight_of_hand':'dex',
    'stealth':'dex',
    'survival':'wis',
    'dexterity_saving_throws':'dex',
    'strength_saving_throws':'str',
    'constitution_saving_throws':'con',
    'intelligence_saving_throws':'int',
    'wisdom_saving_throws':'wis',
    'charisma_saving_throws':'cha'
}

def get_character_json_from_dndb_id(dndb_id):
    with urllib.request.urlopen("https://ddb-character.vttassets.com/" + str(dndb_id)) as url:
        data = json.loads(url.read().decode())['data']

        char = {
            'name':"",
            'abilities':{},
            "skill_bonuses":{x:0 for x in skills},
            'total_level':0,
            'proficiency_bonus':2,
            'initiative_bonus':0,
            "avatar_url": ""
        }

        char['name'] = data['name']

        # Calculate total level
        char['total_level'] = sum([plr_class['level'] for plr_class in data['classes']])

        # Calculate proficiency
        if char['total_level'] < 5:
            char['proficiency_bonus'] = 2
        elif char['total_level'] < 9:
            char['proficiency_bonus'] = 3
        elif char['total_level'] < 13:
            char['proficiency_bonus'] = 4
        elif char['total_level'] < 17:
            char['proficiency_bonus'] = 5
        else:
            char['proficiency_bonus'] = 6

        # Ability bonuses
        for mod_type in ['class', 'race', 'feat']:
            if mod_type in data['modifiers']:
                for pot_bonus in data['modifiers'][mod_type]:
                    if pot_bonus['entityTypeId'] == 1472902489:
                        data['stats'][pot_bonus['entityId']-1]['value'] += pot_bonus['value']

        has_half_prof = False

        # Initiative and skill bonus
        for mod_type in ['class', 'race', 'feat', 'background']:
            if mod_type in data['modifiers']:
                for pot_bonus in data['modifiers'][mod_type]:
                    # Initative bonuses
                    if pot_bonus['subType'] == 'initiative' and pot_bonus['type'] == 'bonus':
                        if pot_bonus['value'] is not None:
                            char['initiative_bonus'] += pot_bonus['value']
                        else:
                            char['initiative_bonus'] += total_to_bonus(data['stats'][pot_bonus['statId']-1]['value'])

                    # Skill bonuses
                    if pot_bonus['modifierTypeId'] == 10 and pot_bonus['subType'] in char['skill_bonuses'] and char['skill_bonuses'][pot_bonus['subType']] < char['proficiency_bonus']:
                        char['skill_bonuses'][pot_bonus['subType']] = char['proficiency_bonus']
                    if pot_bonus['modifierTypeId'] == 12 and pot_bonus['subType'] in char['skill_bonuses'] and char['skill_bonuses'][pot_bonus['subType']] < char['proficiency_bonus'] * 2:
                        char['skill_bonuses'][pot_bonus['subType']] = char['proficiency_bonus'] * 2

                    if pot_bonus['modifierTypeId'] == 13:
                        has_half_prof = True
                    

        # Get ability stats
        char['abilities']['str'] = data['stats'][0]['value']
        char['abilities']['dex'] = data['stats'][1]['value']
        char['abilities']['con'] = data['stats'][2]['value']
        char['abilities']['int'] = data['stats'][3]['value']
        char['abilities']['wis'] = data['stats'][4]['value']
        char['abilities']['cha'] = data['stats'][5]['value']

        # Add dex to initiative
        char['initiative_bonus'] += total_to_bonus(char['abilities']['dex'])

        if has_half_prof:
            char['initiative_bonus'] += int(char['proficiency_bonus'] / 2)

        # Add ability stats to skills
        for skill_name in skills:
            if has_half_prof and char['skill_bonuses'][skill_name] == 0:
                char['skill_bonuses'][skill_name] = int(char['proficiency_bonus'] / 2)
            char['skill_bonuses'][skill_name] += total_to_bonus(char['abilities'][skills[skill_name]])

        if data['avatarUrl'] is not None:
            char['avatar_url'] = data['avatarUrl']
        else:
            char['avatar_url'] = data['race']['portraitAvatarUrl']

        return char