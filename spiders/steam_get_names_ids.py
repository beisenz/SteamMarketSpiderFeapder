# -*- coding: utf-8 -*-
"""
Created on 2024-07-05 16:52:16
---------
@summary:
---------
@author: pc
"""

import re
import urllib
import feapder
from feapder.db.mysqldb import MysqlDB
from items.steam_names_ids_item import SteamNamesIdsItem


class SteamGetNamesIds(feapder.Spider):
    with open('secrets/proxy_api.txt', 'r', encoding='utf-8') as file:
        PROXY_API = file.readline()

    __custom_setting__ = dict(
        PROXY_EXTRACT_API = PROXY_API,  # 代理提取API ，返回的代理分割符为\r\n
        PROXY_ENABLE = True,
        PROXY_MAX_FAILED_TIMES = 5,  # 代理最大失败次数，超过则不使用，自动删除
        PROXY_POOL = "feapder.network.proxy_pool.ProxyPool",  # 代理池

        SPIDER_THREAD_COUNT = 15,
        SPIDER_MAX_RETRY_TIMES = 3,  # 每个请求最大重试次数
    )

    def start_requests(self):
        db = MysqlDB()
        steam_names_dict = db.find('SELECT * FROM steam_names;', to_json=True)

        for temp in steam_names_dict:
            game = temp['game']
            if game == 'dota2':
                gameid = '570'
            elif game == 'csgo':
                gameid = '730'
            market_hash_name = temp['market_hash_name']
            encodename = urllib.parse.quote(market_hash_name)
            url = f'https://steamcommunity.com/market/listings/{gameid}/{encodename}'
            yield feapder.Request(url)

    def parse(self, request, response):
        regex = r'Market_LoadOrderSpread\(\s*(\d+)\s*\)'
        item_nameid_list = re.findall(regex, response.content.decode('utf-8'))

        if item_nameid_list == []:
            yield feapder.Request(request.url)
        else:
            item_nameid = item_nameid_list[0]
        
        if '/570/' in request.url:
            game = 'dota2'
        elif '/730/' in request.url:
            game = 'csgo'
        market_hash_name = self.extract_last_segment(request.url)

        item = SteamNamesIdsItem()
        item.item_nameid = item_nameid
        item.game = game
        item.market_hash_name = market_hash_name
        yield item

    def extract_last_segment(self, url):
        # 使用 urllib.parse 解析 URL
        parsed_url = urllib.parse.urlparse(url)
        # 获取路径部分并分割为列表
        path_segments = parsed_url.path.split('/')
        # 返回最后一个非空段
        return urllib.parse.unquote(path_segments[-1])


if __name__ == "__main__":
    SteamGetNamesIds(redis_key="steam_get_names_ids:filter").start()
