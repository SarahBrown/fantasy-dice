// Minimal fake client to test the server

const socket = io('ws://localhost:5000');
char_sheet = null
player_ls = null
roll_hist = null

socket.on('connect', () => {
    // for test, use set campaign ID and stuff
    campaign_id = "mygame";
    player_name = "jorge";
    dndb_url = "www.example/123456"
    socket.emit('join_campaign', {"name":player_name, "campaign_id":campaign_id, "dndbeyond_url":dndb_url});
    socket.emit('dndbeyond_url', {"url":dndb_url})
  });

socket.on('char_sheet', (char_sheet_json) => {
    // receive and store the JSON characer sheet
    char_sheet = char_sheet_json
  });

socket.on('player_list', (player_list) => {
    // player_list is list of tuples (sid, name, avatar URL) dumped to JSON
    // could change to just list of names if we don't need sid
    player_ls = player_list
  });

socket.on('roll_history', (roll_history) => {
    // roll_history is list dumped to JSON
    roll_hist = roll_history
})

// Haven't done stuff with init_roll yet bc it's complicated

// **************************
// Reference stuff
/*
socket.on('connect', () => {
  // either with send()
  socket.send('Hello!');

  // or with emit() and custom event names
  socket.emit('salutations', 'Hello!', { 'mr': 'john' }, Uint8Array.from([1, 2, 3, 4]));
});

// handle the event sent with socket.send()
socket.on('message', data => {
  console.log(data);
});

// handle the event sent with socket.emit()
socket.on('greetings', (elem1, elem2, elem3) => {
  console.log(elem1, elem2, elem3);
});



socket.emit('join', { 'channel': channel, ... });
socket.emit('send message', {'message': message, 'channel': channel});
*/