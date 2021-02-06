class Player:
    def __init__(self, sid, name:str):
        self.sid = sid
        self.name = name
    
    def __str__(self):
        return "(Player: " + self.name + ", SID: " + self.sid + ")"
