import board
import amazons
import Draughts
import timer
import asyncio
import json
from Surakarta import Surakarta

get_mesg = lambda x: bytes(str(json.dumps(x)), 'utf-8')

class Room():
    def __init__(self, boardtype, boardargs, totaltime, roomId):

        # 初始化棋盘，计时器， 玩家列表， 比赛状态
        self.__board = board.Board()
        self.__timer = timer.Timer(totaltime)
        self.__status = 0
        self.roomId = roomId
        self.type = boardtype
        self.player = []
        self.history = []

        # 根据棋种覆盖原棋盘

        if boardtype == None:
            pass
        elif boardtype == 'amazons':
            self.__board = amazons.Amazons(boardargs[0], boardargs[1])
        elif boardtype == 'Surakarta':
            self.__board = Surakarta()
        elif boardtype == 'Draughts':
            self.__board = Draughts()

    # 加入玩家
    def addPlayer(self, player, order):
        if self.type == 'amazons':
            playerId = 'B' if order == '1' else 'A'
        elif self.type == 'surakarta':
            playerId = 1 if order == '1' else -1
        elif self.type == 'Draughts':
            playerId = 'B' if order == '1' else 'A'

        self.player.append({'id': playerId, 'player': player, 'order': order})
        return playerId

    # 删除玩家
    def removePlayer(self, id):
        playerNum = len(self.player)
        for i in range(playerNum):
            if self.player[i]['id'] == id:
                self.player.pop(i)

        return 1

    # 开始游戏，并开始计时
    async def start(self, playerId):
        self.__status += 1
        if self.__status >= 2:
            mesg = {'mesg': 'start'}
            await self.notifyToAll(mesg)
        else:
            mesg = {'mesg': 'ready'}
            await self.notifyToOther(playerId, mesg)

    async def rollback(self):
        board = self.__board.rollback()
        await self.notifyToAll({'mesg': 'rollback', 'board': board})

    # 获取比赛状态
    def status(self):
        return {'status': self.__status, 'message': None}

    # 移动棋子
    async def move(self, player, location, *kw):
        board, result = self.__board.fire(player, location, *kw)
        self.history.append(board)
        await self.notifyToOther(player, {'mesg': 'move', 'move': location, 'player': player, 'result': result, 'kw': kw[0]})
    
    # 通知另一方玩家
    async def notifyToOther(self, playerId, mesg):
        for i in self.player:
            if i['id'] != playerId:
                await i['player'].send(get_mesg(mesg))

    # 通知所有玩家
    async def notifyToAll(self, mesg):
        for i in self.player:
            await i['player'].send(get_mesg(mesg))

    # 先后手次序
    def getOrder(self):
        if self.player[0]['order'] == '1':
            return '2'
        else:
            return '1'




