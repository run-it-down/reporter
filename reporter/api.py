import json
import requests

import falcon

try:
    import util
except ModuleNotFoundError:
    print('common package not in python path')


ANALYZER_ENDPOINT = 'https://analyzer.run-it-down.lol'

logger = common.util.Logger(__name__)


class Solo:

    def on_get(self, req, resp):
        logger.info(f'solo report for {req.params["summoner"]}')

        # get WR
        params = {
            'summoner': req.params['summonerName']
        }
        wr = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/winrate'), params=params)

        # get KDA
        params = {
            'summoner': req.params['summonerName']
        }
        kda = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/kda'), params=params)

        # get CS
        params = {
            'summoner': req.params['summonerName']
        }
        kda = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/cs'), params=params)

        # aggregate metrics to report
        resp.body = json.dumps({
            'winrate': wr,
            'kda': kda,
            'cs': cs
        })


def create():
    api = falcon.API()
    api.add_route('solo', Solo())
    logger.info('falcon initialized')
    return api


application = create()
