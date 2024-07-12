import pandas as pd
from feapder.db.mysqldb import MysqlDB

db = MysqlDB()

def get_dif(platform_price, order_price):
    platform_price = platform_price
    STEAM_SELL_SERVICE_CHARGE = 0.87 # steam 出售手续费
    BUFF_SELL_SERVICE_CHARGE = 0.965 # buff 出售手续费
    buff_order_price = platform_price * BUFF_SELL_SERVICE_CHARGE # steam 出售到手余额
    steam_order_price = order_price * STEAM_SELL_SERVICE_CHARGE  # buff 出售到手余额
    data = {
        'platform_to_steam': round(platform_price / steam_order_price, 3), # buff购买价格 / steam到手余额
        'steam_to_platform': round(buff_order_price / order_price, 3)      # buff到手余额 / steam购买价格
    }
    return data

def get_steam_graph_dict():
    steam_graph = db.find('select * from steam_graph;', to_json=True)
    steam_graph_dict = {}

    for temp in steam_graph:
        market_hash_name = temp['market_hash_name']
        buy_order_graph = temp['buy_order_graph']
        sell_order_graph = temp['sell_order_graph']
        steam_graph_dict[market_hash_name] = {'buy_order_graph': buy_order_graph, 'sell_order_graph': sell_order_graph}
    
    return steam_graph_dict


parse_data = {}
parse_list = []
db_buff = db.find('select * from buff;', to_json=True)
steam_graph_dict = get_steam_graph_dict()
cant_find_list = []
for buff in db_buff:
    game = buff['game']
    name = buff['name']
    buy_num = buff['buy_num']
    sell_num = int(buff['sell_num'])
    item_id = buff['item_id']
    buy_max_price = float(buff['buy_max_price'])
    sell_min_price = float(buff['sell_min_price'])
    market_hash_name = buff['market_hash_name']

    if list(steam_graph_dict.keys()).count(market_hash_name) == 0:
        cant_find_list.append(name)
        continue
    
    buy_order_graph = steam_graph_dict[market_hash_name]['buy_order_graph']
    sell_order_graph = steam_graph_dict[market_hash_name]['sell_order_graph']
    buy_order_graph = [temp[:2] for temp in buy_order_graph]
    sell_order_graph = [temp[:2] for temp in sell_order_graph]
    
    buy_order_graph_first = buy_order_graph[0] if len(buy_order_graph) > 0 else None
    sell_order_graph_first = sell_order_graph[0] if len(sell_order_graph) > 0 else None
    data = {
        '游戏': game,
        '名称': name,
        'BUFF最低价': sell_min_price,
        'BUFF在售': sell_num,
        'Steam求购最高': buy_order_graph_first[0] if buy_order_graph_first is not None else None,
        '数量_1': buy_order_graph_first[1] if buy_order_graph_first is not None else None,
        'Steam在售最低': sell_order_graph_first[0] if sell_order_graph_first is not None else None,
        '数量_2': sell_order_graph_first[1] if sell_order_graph_first is not None else None,
        'BUFF到Steam求购': get_dif(sell_min_price, buy_order_graph_first[0])['platform_to_steam'] if buy_order_graph_first is not None else None,
        'BUFF到Steam销售': get_dif(sell_min_price, sell_order_graph_first[0])['platform_to_steam'] if sell_order_graph_first is not None else None,
        'Steam到BUFF求购': get_dif(buy_max_price, sell_order_graph_first[0])['steam_to_platform'] if sell_order_graph_first is not None else None,
        'Steam到BUFF销售': get_dif(sell_min_price, sell_order_graph_first[0])['steam_to_platform'] if sell_order_graph_first is not None else None,
        'URL': f'https://buff.163.com/goods/{item_id}'
    }
    parse_list.append(data)

df = pd.DataFrame(parse_list)
df.to_excel('data.xlsx')