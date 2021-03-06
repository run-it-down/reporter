import json
import requests

import falcon
import psutil

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

        # common_games
        logger.info('getting common games')
        game_information = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/common-games'), params=params)
        game_information = json.loads(game_information.content.decode())

        if not game_information:
            resp.status_code = 404
            return

        # get WR
        logger.info('getting wr')
        wr = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/winrate'), params=params)
        wr = json.loads(wr.content.decode())

        # get KDA
        logger.info('getting kda')
        kda = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/kda'), params=params)
        kda = json.loads(kda.content.decode())

        # get CS
        logger.info('getting cs')
        cs = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/cs'), params=params)
        cs = json.loads(cs.content.decode())

        # get avg-game
        logger.info('getting average game')
        avg_game = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/avg-game'), params=params)
        avg_game = json.loads(avg_game.content.decode())

        # millionaire
        logger.info('getting classification millionaire')
        millionaire = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/classification/millionaire'), params=params)
        millionaire = json.loads(millionaire.content.decode())

        # match-type
        logger.info('getting classification match-type')
        match_type = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/classification/match-type'), params=params)
        match_type = json.loads(match_type.content.decode())

        # murderous-duo
        logger.info('getting classification murderous-duo')
        murderous_duo = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/classification/murderous-duo'), params=params)
        murderous_duo = json.loads(murderous_duo.content.decode())

        # duo-type
        logger.info('getting classification duo-type')
        duo_type = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/classification/duo-type'), params=params)
        duo_type = json.loads(duo_type.content.decode())

        # farmer-type
        logger.info('getting classification farmer-type')
        farmer_type = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/classification/farmer-type'), params=params)
        farmer_type = json.loads(farmer_type.content.decode())

        # tactician
        logger.info('getting classification tactician')
        tactician = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/classification/tactician'), params=params)
        tactician = json.loads(tactician.content.decode())

        # champ combination
        logger.info('getting champ combination')
        champ_combo = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/combinations/champions'), params=params)
        champ_combo = json.loads(champ_combo.content.decode())

        # aggression
        logger.info('getting aggression')
        aggression = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/aggression'), params=params)
        aggression = json.loads(aggression.content.decode())

        # avg-role
        logger.info('getting avg-role')
        avg_role = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/avg-role'), params=params)
        avg_role = json.loads(avg_role.content.decode())

        # gold-diff
        logger.info('getting gold-diff')
        gold_diff = requests.get(url=util.urljoin(ANALYZER_ENDPOINT, '/gold-diff'), params=params)
        gold_diff = json.loads(gold_diff.content.decode())

        # aggregate metrics to report
        resp.text = json.dumps({
            'game_information': game_information,
            'winrate': wr,
            'kda': kda,
            'cs': cs,
            'avg-game': avg_game,
            'classification_millionaire':  millionaire,
            'match_type': match_type,
            'murderous_duo': murderous_duo,
            'duo_type': duo_type,
            'farmer_type': farmer_type,
            'tactician': tactician,
            'champ_combo': champ_combo,
            'aggression': aggression,
            'avg_role': avg_role,
            'gold_diff': gold_diff,
        })


class Status:

    def on_get(self, req, resp):
        cpu = psutil.cpu_percent()
        data = '{"cpu": ' + str(cpu) + '}'
        resp.text = data
        resp.status = falcon.HTTP_OK


def create():
    api = falcon.App(cors_enable=True)
    api.add_route('/', Main())
    api.add_route('/status', Status())
    logger.info('falcon initialized')
    return api


application = create()
