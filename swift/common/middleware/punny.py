__author__ = 'imkarrer'

import random
from swift.common import swob
from swift.common import utils

PUNS = [
    "Time flies like an arrow. Fruit flies like a banana.\n",
    "Show me a piano falling down a mineshaft and I'll show you A-flat minor.\n",
    "To write with a broken pencil is pointless.\n",
    "A bicycle can't stand on its own because it is two-tired.\n",
    "Those who get too big for their britches will be exposed in the end.\n",
    "When a clock is hungry it goes back four seconds.\n",
    "The man who fell into an upholstery machine is fully recovered.\n",
    "Bakers trade bread recipes on a knead to know basis.\n",
    "A grenade thrown into a kitchen in France would result in Linoleum Blownapart.\n",
    "When cannibals ate a missionary they got a taste of religion.\n",
    "A steak pun is a rare medium well done.\n",
    "If Shaquille O'Neal was a banana he would be Shaquille O'Peal.\n",
    "If Shaquille O'Neal was a shade of blue green he would be Shaquille O'Teal.\n",
    "If Shaquille O'Neal was overly emotional he would be Shaquille O'Feel.\n",
    "Which American President was least guilty?  Lincoln, we was in a cent.\n",
    "When a marathon runner had ill fitting shoes, he suffered from the agony of defeat.\n",
    "Does the name Pavlov ring a bell?\n",
    "Without geometry, life is pointless.\n",
    "When she told me I was average, she was just being mean.\n",
    "Energizer Bunny arrested - charged with battery.\n",
]

class SwiftPunnyMiddleware(object):

    def __init__(self, app, conf):
        self.app = app
        self.logger = utils.get_logger(conf, log_route='punny')

    def __call__(self, env, start_response):
        req = swob.Request(env)
        # if they want a pun return random index from pun list
        if 'X-Give-Me-A-Pun' in req.headers:
            resp = swob.Response(request=req,
                                 body=(random.choice(PUNS)),
                                 content_type="text/plain",
                                 status=202,
                                 )
            return resp(env, start_response)

        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)

    def punny_filter(app):
        return SwiftPunnyMiddleware(app, conf)
    return punny_filter