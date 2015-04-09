__author__ = 'imkarrer'

import unittest
from swift.common import swob
from swift.common.middleware import punny

class FakeApp(object):
    def __call__(self, env, start_response):
        req = swob.Request(env)
        return swob.Response(request=req, body='FAKE APP')(
            env, start_response)


class TestSwiftPunnyMiddleware(unittest.TestCase):

    def setUp(self):
        self.got_statuses = []

    def get_app(self, app, global_conf, **local_conf):
        factory = punny.filter_factory(global_conf, **local_conf)
        return factory(app)

    def start_response(self, status, headers):
        self.got_statuses.append(status)

    def test_punny(self):
        req = swob.Request.blank('/', environ={'REQUEST_METHOD': 'GET'})
        app = self.get_app(FakeApp(), {})
        resp = app(req.environ, self.start_response)
        self.assertEquals(['200 OK'], self.got_statuses)
        self.assertEquals(resp, ['FAKE APP'])

    def test_punny_pass(self):
        req = swob.Request.blank('/',
                                 environ={'REQUEST_METHOD': 'GET'},
                                 headers={'X-Give-Me-A-Pun': 1},
                                 )
        app = self.get_app(FakeApp(), {})
        resp = app(req.environ, self.start_response)
        self.assertEquals(['202 Accepted'], self.got_statuses)
        self.assertTrue(resp[0] in punny.PUNS)

    def test_punny_fail(self):
        req = swob.Request.blank('/',
                                 environ={'REQUEST_METHOD': 'GET'},
                                 headers={'X-Give-Me-A-Pu': 1},
                                 )
        app = self.get_app(FakeApp(), {})
        resp = app(req.environ, self.start_response)
        self.assertEquals(['200 OK'], self.got_statuses)
        self.assertTrue(resp, ['FAKE APP'])
