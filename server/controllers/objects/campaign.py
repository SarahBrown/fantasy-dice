from controllers.objects.player import Player
from json import dumps

class Campaign:
    # object to store campaign name, list of players, and roll history
    def __init__(self, first_player:Player, campaign_name:str="NO_NAME_PROVIDED"):
        # map of SIDs to Player objects
        self.players = {first_player.sid : first_player}
        # history of roll info (player name, roll purpose, roll result)
        self.roll_history = []
        # name of the campaign (the ID originally provided for it)
        self.campaign_name = campaign_name
    
    # add a newly joined player
    def add_player(self, new_player:Player):
        self.players[new_player.sid] = new_player

    # remove a disconnected player
    def remove_player(self, player_sid):
        self.players.pop(player_sid, None)
    
    # add a roll that has taken place to the roll history.
    # this should update the chat feed with the new roll info as well.
    def new_roll(self, player_sid, roll_purpose:str, roll_result:int):
        self.roll_history.append((self.players[player_sid].name, roll_purpose, roll_result))
    
    # get a JSON list of the players
    def get_player_list_json(self):
        p_list = []
        for p in self.players:
            p_list.append((p.sid, p.name, p.avatar))
        return dumps(p_list)
