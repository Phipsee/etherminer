import requests
import persistence_service

ETHEREUM_BASE_UNIT_FAKTOR = 1_000_000_000_000_000_000

ENDPOINT_ETHERMINER = 'https://api.ethermine.org'
ENDPOINT_ETH_EUR_CONVERTER = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=EUR'

DASHBOARD = '/miner/:miner/dashboard'

REPLY_INFO = 'Current:  :currentHashrate\nReported: :reportedHashrate\nUnpaid: :unpaid / :unpaid_EUR\nEthereum: :ethereumPriceEur'

KEY_CURRENT_HASHRATE = 'currentHashrate'
KEY_REPORTED_HASHRATE = 'reportedHashrate'
KEY_AVERAGE_HASHRATE = 'averageHashrate'
KEY_UNPAID_BALANCE = 'unpaid'
KEY_UNPAID_BALANCE_EUR = 'unpaid_EUR'
KEY_ETHEREUM_PRICE_EUR = 'ethereumPriceEur'


def get_ethereum_amount(wei_amount):
    return wei_amount/ETHEREUM_BASE_UNIT_FAKTOR


def get_ethreum_amount_text(wei_amount):
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
    stats['current_hashrate'] = current_stats[KEY_CURRENT_HASHRATE]
    stats['reported_hashrate'] = current_stats[KEY_REPORTED_HASHRATE]
    stats['unpaid_eth'] = current_stats[KEY_UNPAID_BALANCE]
    stats['eth_eur'] = get_eth_euro()

    persistence_service.insertMiningHistory(stats)

    reply = REPLY_INFO

    reply = reply.replace(':'+KEY_CURRENT_HASHRATE,
                          get_hashrate(stats['current_hashrate']))

    reply = reply.replace(':'+KEY_REPORTED_HASHRATE,
                          get_hashrate(stats['reported_hashrate']))

    reply = reply.replace(':'+KEY_UNPAID_BALANCE_EUR,
                          get_eth2eur(stats['unpaid_eth'],  stats['eth_eur']))

    reply = reply.replace(':'+KEY_UNPAID_BALANCE,
                          get_ethreum_amount_text(stats['unpaid_eth']))

    reply = reply.replace(':'+KEY_ETHEREUM_PRICE_EUR,
                          get_eth2eur(ETHEREUM_BASE_UNIT_FAKTOR, stats['eth_eur']))

    return reply


def get_eth_euro():
    response = requests.get(ENDPOINT_ETH_EUR_CONVERTER)
    if response.status_code != 200:
        return 'error while retrieving eth - eur...'
    return response.json()['EUR']


def get_eth2eur(wei, eur):
    eth = get_ethereum_amount(wei)
    return "{:.2f}".format(eur * eth)+'€'


def doSaveChannelGuild(guild_id, channel_id):
    persistence_service.insertChannelToUse(guild_id, channel_id)


def doRetrieveChannels():
    result = persistence_service.selectChannelsToUse()
    return result
