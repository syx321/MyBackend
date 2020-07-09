import asyncio
import json
import websockets
from room import Room
from amazons import Amazons

get_mesg = lambda x: bytes(str(json.dumps(x)), 'utf-8')


class Server():
    def __init__(self):
        self.__ip = '0.0.0.0'
        self.__port = 5434
        self.__server = websockets.serve(self.handler, self.__ip, self.__port)

        # 房间列表
        self.rooms = []

        # 客户端列表
        self.clients = []

    def start(self):
        print('Starting server')
        asyncio.get_event_loop().run_until_complete(self.__server)
        asyncio.get_event_loop().run_forever()

    # 处理前端消息
    async def handler(self, socket, path):
        self.clients.append(socket)
        print('Client connected')
        # 返回房间列表
        await socket.send(
            get_mesg({'mesg': 'room_list', 'room_list': [{'id': i.roomId, 'type': i.type} for i in self.rooms]}))

        # 接收前端消息并转换成json对象
        data = await socket.recv()
        data = json.loads(data)
        print(data)

        # 判断是添加房间还是加入房间
        if data['mesg'] == 'add_room':
            room = Room(data['type'], data['args'], data['time'], len(self.rooms) + 1)
            self.rooms.append(room)
            order = data['order']
            for i, c in enumerate(self.clients):
                if c != socket:
                    try:
                        await c.send(get_mesg(
                            {'mesg': 'room_list', 'room_list': [{'id': i.roomId, 'type': i.type} for i in self.rooms]}))
                    except websockets.exceptions.ConnectionClosedOK:
                        self.clients.remove(c)

        elif data['mesg'] == 'join':
            room = self.rooms[int(data['room_id']) - 1]
            order = room.getOrder()
        playerId = room.addPlayer(socket, order)

        # 返回房间和玩家信息
        await socket.send(get_mesg({'mesg': data['mesg'], 'playerId': playerId, 'type': room.type, 'order': order}))

        # 等待进一步操作(开始 / 移动 / 悔棋)
        while True:
            data = await socket.recv()
            data = json.loads(data)
            print(data)

            if (data['mesg'] == 'start'):
                await room.start(playerId)
            elif (data['mesg'] == 'move'):
                location = data['location']
                if data.get('kw') != None:
                    await room.move(playerId, location, data['kw'])
                else:
                    await room.move(playerId, location)
            elif (data['mesg'] == 'rollback'):
                await room.rollback()


if __name__ == '__main__':
    server = Server()
    server.start()
