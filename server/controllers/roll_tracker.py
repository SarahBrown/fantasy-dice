from typing import List, Tuple
from objects.player import Player
from objects.campaign import Campaign

class Roll_tracker:
    # dict mapping campaign_id to Campaign object
    campaigns = {}
    # dict that maps player ID to the campaign they are in
    player_in_campaign = {}

    @staticmethod
    def join_campaign(sid, name, campaign_id):

        # player is already in a campaign, but we shouldn't see this happen
        if sid in Roll_tracker.player_in_campaign:
            return
        
        # make the player object
        new_player = Player(sid, name)

        # if the campaign doesn't exist, make it & add to dict of campaigns
        if not campaign_id in Roll_tracker.campaigns:
            Roll_tracker.campaigns[campaign_id] = Campaign([new_player], campaign_id)
        # if the campaign already exists, add the player
        else:
            Roll_tracker.campaigns[campaign_id].add_player(new_player)

        # keep record of which campaign a player is in
        Roll_tracker.player_in_campaign[sid] = campaign_id

        print(Roll_tracker.campaigns)
        print(Roll_tracker.player_in_campaign)

    @staticmethod
    # remove a player from everything when they disconnect.
    # don't remove their previous rolls from a campaign's roll history.
    def remove_player(sid):
        # figure out which campaign this player is in
        campaign = Roll_tracker.player_in_campaign[sid]
        # remove the player from the list of (sid, campaign)
        del Roll_tracker.player_in_campaign[sid]
        # remove the player from their campaign's list of players
        campaign.remove_player(sid)

        # if no one is left in the campaign, delete it
        if len(Roll_tracker.campaigns[campaign].players) < 1:
            del Roll_tracker.campaigns[campaign]

    @staticmethod
    # get a new roll to be added to the history and displayed to everyone in the chat
    def receive_roll(sid, roll_purpose:str, roll_result:int):
        # find which campaign the player is in
        campaign_id = Roll_tracker.player_in_campaign[sid]
        # add the roll to that campaign's history
        Roll_tracker.campaigns[campaign_id].new_roll(sid,roll_purpose,roll_result)

    @staticmethod
    def get_roll_history(campaign_id):
        return Roll_tracker.campaigns[campaign_id].roll_history
    
    @staticmethod
    def get_player_list(campaign_id):
        return Roll_tracker.campaigns[campaign_id].players
    
    @staticmethod
    def reset():
        # reset all players and campaigns
        Roll_tracker.campaigns = {}
        Roll_tracker.player_in_campaign = {}

