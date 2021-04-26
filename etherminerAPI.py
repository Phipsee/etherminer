import requests

ETHEREUM_BASE_UNIT_FAKTOR = 1_000_000_000_000_000_000

ENDPOINT_ETHERMINER = 'https://api.ethermine.org'

DASHBOARD = '/miner/:miner/dashboard'

REPLY_INFO = 'Current:  :currentHashrate\nReported: :reportedHashrate\nUnpaid: :unpaid'

KEY_CURRENT_HASHRATE = 'currentHashrate'
KEY_REPORTED_HASHRATE = 'reportedHashrate'
KEY_AVERAGE_HASHRATE = 'averageHashrate'
KEY_UNPAID_BALANCE = 'unpaid'


def get_ethreum_amount(wei_amount):
    return "{:.6f}".format(wei_amount/ETHEREUM_BASE_UNIT_FAKTOR)+' ETH'


def get_hashrate(hashrate):
    modifier = 0
    while (hashrate / 1000) > 1:
        hashrate = hashrate / 1000
        modifier = modifier + 1

    result = "{:.2f}".format(hashrate)+' '

    if (modifier == 0):
        return result+'H/s'
    elif (modifier == 1):
        return result + 'kH/s'
    elif (modifier == 2):
        return result + 'MH/s'
    elif (modifier == 3):
        return result + 'GH/s'
    elif (modifier == 4):
        return result + 'TH/s'


def execute_request(minerId, target):
    url = ENDPOINT_ETHERMINER + target.replace(':miner', minerId)

    return requests.get(url)


def get_info(minerId):
    response = execute_request(minerId, DASHBOARD)

    if response.status_code != 200:
        return 'Error retrieving data'

    current_stats = response.json()['data']['currentStatistics']

    stats = {}
    reply = REPLY_INFO

    reply = reply.replace(':'+KEY_CURRENT_HASHRATE,
                          get_hashrate(current_stats[KEY_CURRENT_HASHRATE]))

    reply = reply.replace(':'+KEY_REPORTED_HASHRATE,
                          get_hashrate(current_stats[KEY_REPORTED_HASHRATE]))

    reply = reply.replace(':'+KEY_UNPAID_BALANCE,
                          get_ethreum_amount(current_stats[KEY_UNPAID_BALANCE]))

    return reply


print(get_info('4744B5AD9494Ea1569051694Cc548a7d3140FB01'))
