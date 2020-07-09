import time

class Timer(object):
    def __init__(self, total):
        self.players = {"A" : 0}
        self.total = total
        self.curr_time = time.time()
        self.curr_player = "A"

    def toggle(self, player):
        if (player not in self.players):
            self.players[player] = 0
        self.players[self.curr_player] = time.time() - self.curr_time
        self.curr_player = player
        self.curr_time = time.time()
        
        return self.players

    def timeout(self, player):
        if (player in self.players):
            return self.total - (time.time() - self.curr_time) - self.players[player]
        else:
            return -1

    def pause(self):
        self.is_pause = True
        self.pause_time = time.time()



'''
if __name__ == "__main__":
    t = Timer(20)
    time.sleep(10)
    t.toggle("B")
    print(t.timeout("A"))
    print(t.timeout("B"))
    t.toggle("A")
    time.sleep(5)
    t.toggle("C")
    print(t.players)
'''

