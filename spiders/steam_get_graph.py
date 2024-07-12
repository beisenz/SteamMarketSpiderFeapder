# -*- coding: utf-8 -*-
"""
Created on 2024-07-03 08:53:58
---------
@summary:
---------
@author: pc
"""

import json
import feapder
from items.steam_graph_item import SteamGraphItem
from feapder.db.mysqldb import MysqlDB


class Steam(feapder.Spider):
    with open('secrets/proxy_api.txt', 'r', encoding='utf-8') as file:
        PROXY_API = file.readline()

    __custom_setting__ = dict(
    PROXY_EXTRACT_API = PROXY_API,  # 代理提取API ，返回的代理分割符为\r\n
    PROXY_ENABLE = True,
    PROXY_MAX_FAILED_TIMES = 5,  # 代理最大失败次数，超过则不使用，自动删除
    PROXY_POOL = "feapder.network.proxy_pool.ProxyPool",  # 代理池

    SPIDER_THREAD_COUNT = 30,
    )
    def start_requests(self):
        db = MysqlDB()
        steam_names_ids = db.find('SELECT market_hash_name,item_nameid FROM steam_names_ids;', to_json=True)
        steam_names_ids_dict = {}
        for temp in steam_names_ids:
            market_hash_name = temp['market_hash_name']
            item_nameid = temp['item_nameid']
            steam_names_ids_dict[market_hash_name] = item_nameid
        
        buff_market_hash_name = db.find('select market_hash_name from buff;', to_json=True)
        for temp in buff_market_hash_name:
            market_hash_name = temp['market_hash_name']
            item_nameid = steam_names_ids_dict.get(market_hash_name)
            if item_nameid != None:
                url = "https://steamcommunity.com/market/itemordershistogram"
                params = {
                    "country": "CN",
                    "language": "schinese",
                    "currency": "23",
                    "item_nameid": str(item_nameid)
                }
                yield feapder.Request(url, params=params, method="GET", callback=self.parse, item={'market_hash_name': market_hash_name})

    def parse(self, request, response):
        item = SteamGraphItem()
        item.item_nameid = request.params['item_nameid']
        item.market_hash_name = request.item['market_hash_name']
        item.buy_order_graph = json.dumps(response.json['buy_order_graph'], ensure_ascii=False)
        item.sell_order_graph = json.dumps(response.json['sell_order_graph'], ensure_ascii=False)
        yield item

if __name__ == "__main__":
    Steam(redis_key="steam_get_graph:filter").start()
