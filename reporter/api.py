import json
import requests

import falcon

try:
    import util
except ModuleNotFoundError:
    print('common package not in python path')


ANALYZER_ENDPOINT = 'https://analyzer.run-it-down.lol'

logger = util.Logger(__name__)


class Main:

    def on_get(self, req, resp):
        logger.info('reporting')

        # get WR
        params = {
            'summoner1': req.params['summoner1'],
            'summoner2': req.params['summoner2']
        }
        wr = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/winrate'), params=params)

        # get KDA
        params = {
            'summoner1': req.params['summoner1'],
            'summoner2': req.params['summoner2']
        }
        kda = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/kda'), params=params)

        # get CS
        params = {
            'summoner1': req.params['summoner1'],
            'summoner2': req.params['summoner2']
        }
        cs = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/cs'), params=params)

        logger.info(wr.content)
        logger.info(kda.content)
        logger.info(cs.content)

        # aggregate metrics to report
        resp.body = json.dumps({
            'winrate': json.loads(wr.content),
            'kda': json.loads(kda.content),
            'cs': json.loads(cs.content),
        })


def create():
    api = falcon.API()
    api.add_route('/', Main())
    logger.info('falcon initialized')
    return api


application = create()
