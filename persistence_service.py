import urllib.parse
import globals
from pymongo import MongoClient
from datetime import datetime


client = MongoClient(globals.DB_HOST, username=globals.DB_USER, password=globals.DB_PASSWORD,
                     authSource=globals.DB_DATABASE, authMechanism='SCRAM-SHA-1')

ethermine_db = client[globals.DB_DATABASE]


def insertMiningHistory(history_row):
    history_row['created_date'] = datetime.now()
    ethermine_db['mining_history'].insert_one(history_row)


def insertPayoutHistory(history_row):
    history_row['created_date'] = datetime.now()
    ethermine_db['payout_history'].insert_one(history_row)


def insertChannelToUse(guild_id, channel_id):
    ethermine_db['instance_properties'].insert_one(
        {'guild': guild_id, 'channel': channel_id})


def selectChannelsToUse():
    return ethermine_db['instance_properties'].distinct('channel')
