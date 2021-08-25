import unittest

import fakeredis

from store import Store,Storage

server = fakeredis.FakeServer()

class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store(Storage())
        self.server = fakeredis.FakeServer()
        self.store.storage.server = fakeredis.FakeRedis(server=self.server)
        self.store.set('foo','bar')

    def test_get(self):
        self.server.connected = True
        self.assertEqual(self.store.get('foo'),'bar')
        self.assertIsNone(self.store.get('wow'))
        self.store.cache_set('foo','not_bar')
        self.server.connected = False
        self.assertEqual(self.store.get('foo'), 'not_bar')
        self.assertRaises(ConnectionError, self.store.get, 'foo', False)
        self.store.cache_set('foo', 'bar')


    def test_cache_get(self):
        self.assertEqual(self.store.cache_get('foo'),'bar')


    def test_connection_failed(self):
        self.server.connected = False
        self.assertRaises(ConnectionError, self.store.get,'foo', False)

    def test_connection_ok(self):
        self.server.connected = True
        self.assertEqual(self.store.get('foo'),'bar', False)
        
        
    if __name__ == "__main__":
        unittest.main()
