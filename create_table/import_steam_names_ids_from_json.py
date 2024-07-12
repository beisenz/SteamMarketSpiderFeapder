'''
steam_names.json steam_names_ids.json 为长久不可变数据，可以导出为json存储
转移环境时可由json从新导入mysql，此脚本正为此用
'''
import json
from feapder.db.mysqldb import MysqlDB

with open('create_table/steam_names.json', mode='r', encoding='utf-8') as file:
    steam_names_list = json.loads(file.read())

with open('create_table/steam_names_ids.json', mode='r', encoding='utf-8') as file:
    steam_names_ids_list = json.loads(file.read())

db = MysqlDB()

for temp in steam_names_list:
    game = temp['game']
    market_hash_name = temp['market_hash_name']
    db.add_smart('steam_names', {'game': game, 'market_hash_name': market_hash_name})

for temp in steam_names_ids_list:
    game = temp['game']
    market_hash_name = temp['market_hash_name']
    item_nameid = temp['item_nameid']
    db.add_smart('steam_names_ids', {'game': game, 'market_hash_name': market_hash_name, 'item_nameid': item_nameid})