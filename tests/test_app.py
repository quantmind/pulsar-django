"""Tests django chat application"""
import unittest
import asyncio
import json

from pulsar.api import send, get_application
from pulsar.apps import http, ws

from djchat import server


async def start_server(actor, name, argv):
    server(argv)
    await asyncio.sleep(0.5)
    app = await get_application(name)
    return app.cfg


class MessageHandler(ws.WS):

    def __init__(self, loop):
        self.queue = asyncio.Queue(loop=loop)

    def get(self):
        return self.queue.get()

    def on_message(self, websocket, message):
        return self.queue.put(message)


class TestDjangoChat(unittest.TestCase):
    concurrency = 'process'
    app_cfg = None

    @classmethod
    async def setUpClass(cls):
        name = cls.__name__.lower()
        argv = [__file__, 'pulse',
                '-b', '127.0.0.1:0',
                '--concurrency', cls.concurrency,
                '--pulse-app-name', name,
                '--data-store', 'pulsar://127.0.0.1:6410/1']
        cls.app_cfg = await send('arbiter', 'run', start_server, name, argv)
        addr = cls.app_cfg.addresses[0]
        cls.uri = 'http://{0}:{1}'.format(*addr)
        cls.ws = 'ws://{0}:{1}/message'.format(*addr)
        cls.http = http.HttpClient()

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)

    async def test_home(self):
        result = await self.http.get(self.uri)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers['content-type'],
                         'text/html; charset=utf-8')

    async def test_404(self):
        result = await self.http.get('%s/bsjdhcbjsdh' % self.uri)
        self.assertEqual(result.status_code, 404)

    async def test_websocket(self):
        c = self.http
        ws = await c.get(self.ws, websocket_handler=MessageHandler(c._loop))
        response = ws.handshake
        self.assertEqual(response.status_code, 101)
        self.assertEqual(response.headers['upgrade'], 'websocket')
        self.assertEqual(response.connection, ws.connection)
        self.assertTrue(ws.connection)
        self.assertIsInstance(ws.handler, MessageHandler)
        # send a message
        ws.write('Hi there!')
        message = await ws.handler.queue.get()
        self.assertTrue(message)
        data = json.loads(message)
        self.assertEqual(data['message'], 'Hi there!')
        self.assertEqual(data['channel'], 'webchat')
        self.assertFalse(data['authenticated'])
        #
        # close connection
        ws.write_close()
        await ws.connection.event('connection_lost').waiter()
