from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
import json
import random
import logging
import eventlet
import socketio
import time
from controllers.roll_tracker import Roll_tracker
from functions.dndb_json_to_csv import get_character_json_from_dndb_id
from json import loads
from flask_cors import CORS
from vision.tess_test import get_dice


sio = socketio.Server(cors_allowed_origins='*')
app2 = Flask(__name__)
CORS(app2)
app = socketio.WSGIApp(sio, app2)

#@socketio.on('connect')
@sio.event
def connect(sid, environ): 
    print('connect ', sid)

#@socketio.on('join_campaign')
# campaigns are rooms
@sio.event
def join_campaign(sid, name, campaign_id, dndbeyond_url):
    # make sure player name and campaign are alphanumeric and within the allowed lengths
    if str.isalnum(name) and str.isalnum(campaign_id) and 2 < len(name) < 40 and 2 < len(campaign_id) < 40:
        # lowercase campaign to make it easy to type
        campaign_id = str.lower(campaign_id)
        print('received_player_info ', sid)
        # we need the numbers at the end of the URL for the player's DnD Beyond ID.
        # first make sure there isn't a / at the very end
        dndbeyond_url.strip("/")
        # isolate the user ID
        user_id = int(dndbeyond_url[dndbeyond_url.rfind("/")+1:])
        # call Noah's script to generate a JSON char sheet from the DND Beyond profile
        char_sheet_json = get_character_json_from_dndb_id(user_id)
        # convert this string to an actual json object
        char_sheet_str = json.dumps(char_sheet_json)
        # grab the avatar URL from the char sheet
        avatar_url = char_sheet_json["avatar_url"] #TODO check this variable name
        # create player and assign to campaign
        Roll_tracker.join_campaign(sid, name, campaign_id, avatar_url)
        # put up the roll history and list of players
        sio.enter_room(sid, campaign_id)
        #sio.emit('joined_campaign', campaign=campaign_id, player=sid)
        sio.emit('joined_campaign', {'campaign_id': campaign_id, "player": sid}, room=campaign_id)
        #sio.emit('player_list', Roll_tracker.get_player_list(campaign_id), room=campaign_id)
        sio.emit('player_list', {'player_list': Roll_tracker.get_player_list(campaign_id)}, room=campaign_id)
        #sio.emit('roll_history', Roll_tracker.get_roll_history(campaign_id), room=campaign_id)
        sio.emit('roll_history', {'roll_history': Roll_tracker.get_roll_history(campaign_id)}, room=campaign_id)
        # send out the str JSON character sheet
        sio.emit('char_sheet', {'char_sheet': char_sheet_str}, room=sid)

# These are bad but just trying to make this work rn okay
current_cam_campaign = None
current_roll_info = []

#@socketio.on('init_roll')
# when the client presses a button to initiate a roll,
# the client code uses the char sheet to tell them what dice to roll.
# it then tells the server (us) that a roll is happening, and we 
# need to tell the openCV code to init. When the openCV gets the result,
# they send it back to the server (us) and we announce the roll 
# & update the roll history.
@sio.event
def init_roll(sid, roll_purpose:str, roll_modifier:int):
    global current_cam_campaign, current_roll_info
    current_roll_info = [sid, roll_purpose, roll_modifier]
    # TODO get link to video stream of dice rolling
    stream_link = "localhost" + "/video"
    # identify the campaign to which the player belongs
    campaign_id = Roll_tracker.player_in_campaign[sid]

    current_cam_campaign = campaign_id
    roll_purpose_global = roll_purpose

    # return the link to the stream to all players in that campaign
    #sio.emit('stream_link', stream_link, room=campaign_id)
    sio.emit('stream_link', {'stream_link': stream_link}, room=campaign_id)

    # send a request to openCV stuff and wait for a reply with the result

#@socketio.on('disconnect')
@sio.event
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
        if Roll_tracker.does_campaign_exist(campaign_id):
            sio.emit('player_list', {'player_list': Roll_tracker.get_player_list(campaign_id)}, room=campaign_id)

@app2.route('/test/<int:roll_val>/<int:roll2_val>')
def hello_world(roll_val, roll2_val):
    global current_cam_campaign, current_roll_info
    if current_cam_campaign is not None:
        campaign_id = current_cam_campaign
        sid = current_roll_info[0]
        roll_purpose = current_roll_info[1]
        roll_modifier = current_roll_info[2] 

        #roll_result = get_dice(roll_purpose)
        roll_result = roll_val + roll2_val

        # add the relevant modifier determined from the character sheet by the client
        # and passed to this method.
        roll_result += roll_modifier

        # send the result of the roll to the client for a special display
        #sio.emit('new_roll_result', roll_result, campaign=campaign_id)
        sio.emit('new_roll_result', {'roll_result': roll_result}, room=campaign_id)
        # add the new roll to the campaign's roll history
        Roll_tracker.receive_roll(sid, roll_purpose + "+" + str(roll_modifier), roll_result)
        # send new roll history to update the chat display
        #sio.emit('roll_history', Roll_tracker.get_roll_history(campaign_id), room=campaign_id)
        sio.emit('roll_history', {'roll_history': Roll_tracker.get_roll_history(campaign_id)}, room=campaign_id)
        current_cam_campaign = None
        return 'ok'
    else:
        return 'no info but ok'

# def gen():
#     while True:
#         with open("test" + str(random.randint(1,3)) + ".jpg","rb") as f:
#             yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + f.read() + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    #socketio.run(app)

# Referenced the following repo to convert socket IO to work with Flash:
# https://github.com/dxue2012/python-webcam-flask/blob/master/app.py