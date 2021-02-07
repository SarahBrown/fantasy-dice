from makeup_artist import Makeup_artist
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64
#import eventlet
#import socketio
from controllers.roll_tracker import Roll_tracker
from functions.dndb_json_to_csv import get_character_json_from_dndb_id

# sio = socketio.Server(cors_allowed_origins='*')
# app = socketio.WSGIApp(sio)

app = Flask(__name__)
socketio = SocketIO(app)
camera = Camera(Makeup_artist())

@socketio.on('connect')
def connect(sid, environ): 
    print('connect ', sid)
    # users will be asked their name before being allowed to connect

@socketio.on('dndbeyond_url')
def get_char_sheet(sid, url:str):
    # identify the campaign to which the player belongs
    campaign_id = Roll_tracker.player_in_campaign[sid]
    # we need the numbers at the end of the URL.
    # first make sure there isn't a / at the very end
    url.strip("/")
    # isolate the user ID
    user_id = int(url[url.rfind("/"):])
    # call Noah's script to generate a JSON char sheet from the 
    #   DND Beyond profile, and emit it back to the client.
    char_sheet_json = get_character_json_from_dndb_id(user_id)
    emit('char_sheet', {'char_sheet': char_sheet_json}, room=campaign_id)

@socketio.on('init_roll')
# when the client presses a button to initiate a roll,
# the client code uses the char sheet to tell them what dice to roll.
# it then tells the server (us) that a roll is happening, and we 
# need to tell the openCV code to init. When the openCV gets the result,
# they send it back to the server (us) and we announce the roll 
# & update the roll history.
def init_roll(sid, roll_purpose:str, roll_modifier:int):
    # TODO get link to video stream of dice rolling
    stream_link = "TEMP.com"
    # identify the campaign to which the player belongs
    campaign_id = Roll_tracker.player_in_campaign[sid]
    # return the link to the stream to all players in that campaign
    #sio.emit('stream_link', stream_link, room=campaign_id)
    emit('stream_link', {'stream_link': stream_link}, room=campaign_id)
    # TODO send a request to openCV stuff and wait for a reply with the result
    roll_result = -1

    # add the relevant modifier determined from the character sheet by the client
    # and passed to this method.
    roll_result += roll_modifier
    # send the result of the roll to the client for a special display
    #sio.emit('new_roll_result', roll_result, campaign=campaign_id)
    emit('new_roll_result', {'roll_result': roll_result}, room=campaign_id)
    # add the new roll to the campaign's roll history
    Roll_tracker.receive_roll(sid, roll_purpose, roll_result)
    # send new roll history to update the chat display
    #sio.emit('roll_history', Roll_tracker.get_roll_history(campaign_id), room=campaign_id)
    emit('roll_history', {'roll_history': Roll_tracker.get_roll_history(campaign_id)}, room=campaign_id)

@socketio.on('join_campaign')
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
        sio.join_room(sid, campaign_id)
        #sio.emit('joined_campaign', campaign=campaign_id, player=sid)
        emit('joined_campaign', {'campaign_id': campaign_id, "player": sid}, room=campaign_id)
        #sio.emit('player_list', Roll_tracker.get_player_list(campaign_id), room=campaign_id)
        emit('player_list', {'player_list': Roll_tracker.get_player_list(campaign_id)}, room=campaign_id)
        #sio.emit('roll_history', Roll_tracker.get_roll_history(campaign_id), room=campaign_id)
        emit('roll_history', {'roll_history': Roll_tracker.get_roll_history(campaign_id)}, room=campaign_id)

@socketio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)
    # remove person from the list
    # important so refreshing does not keep increasing the number of people
    if sid in Roll_tracker.player_in_campaign:
        campaign_id = Roll_tracker.player_in_campaign[sid]
        #sio.leave_room(sid, campaign_id) # TODO check this works
        Roll_tracker.remove_player(sid)
        # update the player list display
        #sio.emit('player_list', Roll_tracker.get_player_list(campaign_id), room=campaign_id)
        emit('player_list', {'player_list': Roll_tracker.get_player_list(campaign_id)}, room=campaign_id)

if __name__ == '__main__':
    #eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    socketio.run(app)

# Referenced the following repo to convert socket IO to work with Flash:
# https://github.com/dxue2012/python-webcam-flask/blob/master/app.py