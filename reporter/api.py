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
        params = {
            'summoner1': req.params['summoner1'],
            'summoner2': req.params['summoner2']
        }

        # get WR
        logger.info('getting WR')
        wr = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/winrate'), params=params)

        # get KDA
        logger.info('getting KDA')
        kda = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/kda'), params=params)

        # get CS
        logger.info('getting CS')
        cs = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/cs'), params=params)

        # get avg-game
        avg_game = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/avg-game'), params=params)

        # millionaire
        millionaire = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/avg-game'), params=params)

        # match-type
        match_type = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/match-type'), params=params)

        # murderous-duo
        murderous_duo = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/murderous-duo'), params=params)

        # duo-type
        duo_type = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/duo-type'), params=params)

        # farmer-type
        farmer_type = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/farmer-type'), params=params)

        # tactician
        tactician = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/tactician'), params=params)

        # aggregate metrics to report
        resp.body = json.dumps({
            'winrate': json.loads(wr.content),
            'kda': json.loads(kda.content),
            'cs': json.loads(cs.content),
            'avg-game': json.loads(avg_game.content),
            'classification_millionaire':  json.loads(millionaire.content),
            'match_type': json.loads(match_type),
            'murderous_duo': json.loads(murderous_duo),
            'duo_type': json.loads(duo_type),
            'farmer_type': json.loads(farmer_type),
            'tactician': json.loads(tactician),
        })


def create():
    api = falcon.API()
    api.add_route('/', Main())
    logger.info('falcon initialized')
    return api


application = create()
