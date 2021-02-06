import eventlet
import socketio
from controllers.roll_tracker import Roll_tracker

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ): 
    print('connect ', sid)
    # users will be asked their name before being allowed to connect

@sio.event
# campaigns are rooms
def join_campaign(sid, name, campaign_id):
    # make sure player name and campaign are alphanumeric and within the allowed lengths
    if str.isalnum(name) and str.isalnum(campaign_id) and 2 < len(name) < 12 and 2 < len(campaign_id) < 12:
        # lowercase campaign to make it easy to type
        campaign_id = str.lower(campaign_id)
        print('received_name ', sid)
        # create player and assign to campaign
        Roll_tracker.join_campaign(sid, name, campaign_id)
        # put up the roll history and list of players
        sio.enter_campaign(sid, campaign_id)
        sio.emit('joined_campaign', campaign=campaign_id, player=sid)
        sio.emit('player_list', Roll_tracker.get_player_list(campaign_id), campaign=campaign_id)
        sio.emit('roll_history', Roll_tracker.get_roll_history(campaign_id), campaign=campaign_id)

# @sio.event
# def start(sid):
#     campaign_id = Roll_tracker.player_in_campaign[sid]
#     print('starting')
    # # don't allow start game until certain number of players are in
    # min_players = 1
    # if len(Roll_tracker.campaigns[campaign_id].players) >= min_players: 
    #     # Do stuff to start the game

@sio.event
# a player has initiated a roll. we have their SID,
# the roll purpose (DEX save, attack roll, etc),
# and mod in {1:advantage, -1:disadvantage, 0:neither}
def receive_roll_request(sid, roll_purpose:str, mod:int):
    print('received_roll_request ', sid)
    # TODO use character sheet to inform rolls + modifiers
    # TODO make method for creating a new roll template
    # TODO receive advantage, disad, or neither

    # TODO tell the user what kind of roll to make based on roll_purpose & char sheet.
    #   don't need to tell them modifiers, just the dice, since we handle that here

    # TODO have the user make the roll and get the result, or compute it ourselves
    roll_result = None

    # identify the campaign to which the player belongs
    campaign_id = Roll_tracker.player_in_campaign[sid]
    # send the result of the roll for a special display
    sio.emit('new_roll_result', roll_result, campaign=campaign_id)
    # add the new roll to the campaign's roll history
    Roll_tracker.receive_roll(sid, roll_purpose, roll_result)
    # send new roll history to update the chat display
    sio.emit('roll_history', Roll_tracker.get_roll_history(campaign_id), campaign=campaign_id)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    # remove person from the list
    # important so refreshing does not keep increasing the number of people
    if sid in Roll_tracker.player_in_campaign:
        campaign_id = Roll_tracker.player_in_campaign[sid]
        sio.leave_campaign(sid, campaign_id) # TODO check this works
        Roll_tracker.remove_player(sid)
        # update the player list display
        sio.emit('player_list', Roll_tracker.get_player_list(campaign_id), campaign=campaign_id)
        

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)