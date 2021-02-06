import eventlet
import socketio
# from controllers.game_logic import game_logic
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

@sio.event
def start(sid):
    campaign_id = Roll_tracker.player_in_campaign[sid]

    print('starting')
    # don't allow start game until certain number of players TODO change this
    min_players = 1
    if len(Roll_tracker.campaigns[campaign]) >= min_players: 
        # create initial set of dice and send to everyone
        dice_list = game_logic.generate_dice(num_dice=3)
        sio.emit('new_dice', dice_list, campaign=campaign)
        # put up leaderboard with everyone (with all 0 score)
        sio.emit('leaderboard', Roll_tracker.get_leaderboard(campaign), campaign=campaign)

@sio.event
def receive_roll_request(sid, roll_purpose:str):
    print('received_roll_request ', sid)
    # TODO use character sheet to inform rolls + modifiers
    # TODO make method for creating a new roll template
    # TODO receive advantage, disad, or neither
    # check for cheat codes
    if answer == 3141:
        # give a lot of points
        Roll_tracker.update_score(sid, points=15)
        print('Cheater! ', sid)
    # check for reset code
    elif answer == 6282:
        # reset
        Roll_tracker.reset()
    # check if result is correct
    elif game_logic.check_result(answer):
        # result is correct, so add to the user's score
        Roll_tracker.update_score(sid, points=1)
    # result is incorrect
    else:
        sio.emit("incorrect", room=sid)
        # return instead of generating new dice
        return

    campaign = Roll_tracker.playercampaign[sid]
    
    # generate new dice and update leaderboard
    dice_list = game_logic.generate_dice(num_dice=3)
    sio.emit('new_dice', dice_list, room=campaign)
    sio.emit('leaderboard', Roll_tracker.get_leaderboard(campaign), room=campaign)
    return

@sio.event
def health(sid, data):
    print('health ', data)
    # send "health" back to requesters
    sio.emit("health", room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    # remove person from the list
    # important so refreshing does not keep increasing the number of people
    if sid in Roll_tracker.playercampaign:
        campaign = Roll_tracker.playercampaign[sid]
        sio.leave_campaign(sid, campaign)
        Roll_tracker.remove_player(sid)

        # if the campaign still exists, update everyone
        if campaign in Roll_tracker.campaigns:
            sio.emit('leaderboard', Roll_tracker.get_leaderboard(campaign), room=campaign)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)