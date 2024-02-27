import string, random

class Constants:
    HEADER_SIZE = 16
    UDP_PACKET_SIZE = 8096
    RANDOM_ID_CHARS = string.ascii_letters+string.digits

class Utility():
    @staticmethod
    def random_identifier(length:int=12):
        """generate a random id with a certain length"""
        return "".join(
            random.choice(Constants.RANDOM_ID_CHARS)\
            for _ in range(length))

class ClientModel():
    def __init__(self):
        self.is_in_game = False
        self.game_id = None
    
    def set_game_id(self, id:str):
        self.is_in_game = True
        self.game_id = id

class ServerGameData():
    def __init__(self):
        self.client_ids = []
    
    def add_client(self, cid:str):
        self.client_ids.append(cid)
    
    def remove_client(self, cid:str):
        if cid in self.client_ids:
            self.client_ids.remove(cid)

class ServerGameManager():
    def __init__(self):
        self.games = {}
    
    def create_new_game(self):
        gid = Utility.random_identifier(12)
        self.games[gid] = ServerGameData()
    
    def remove_empty_games(self):
        # Remove any games in self.games that have no client_ids
        pass