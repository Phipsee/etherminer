import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DB_USER = config['DB']['USER']
DB_PASSWORD = config['DB']['PASSWORD']
DB_HOST = config['DB']['HOST']
DB_PORT = config['DB']['PORT']
DB_DATABASE = config['DB']['DATABASE']

TOKEN_DISCORD_BOT = config['TOKEN']['DISCORD_BOT']
TOKEN_HEX_MINER = config['TOKEN']['HEX_MINER']
