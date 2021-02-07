class Player:
    def __init__(self, sid, name:str):
        self.sid = sid
        self.name = name
        # TODO include link to DnD beyond photo?
    
    def __str__(self):
        return "(Player: " + self.name + ", SID: " + self.sid + ")"
