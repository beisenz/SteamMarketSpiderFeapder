# -*- coding: utf-8 -*-
"""
Created on 2024-07-04 02:32:20
---------
@summary:
---------
@author: pc
"""

import math
import feapder
from items.steam_names_item import SteamNamesItem

class SteamGetNames(feapder.Spider):
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
        csgo_total_count = 21471
        for i in range(0, math.ceil(csgo_total_count / 100)):
            url = f"https://steamcommunity.com/market/search/render/?norender=1&query=&start={100 * i}&count={100 * i + 100}&search_descriptions=0&sort_column=name&sort_dir=asc&appid=730"
            yield feapder.Request(url)

        dota2_total_count = 38312
        for i in range(0, math.ceil(dota2_total_count / 100)):
            url = f"https://steamcommunity.com/market/search/render/?norender=1&query=&start={100 * i}&count={100 * i + 100}&search_descriptions=0&sort_column=name&sort_dir=asc&appid=570"
            yield feapder.Request(url)

    def parse(self, request, response):
        if response.json['total_count'] == 0:
            yield feapder.Request(request.url)

        for temp in response.json['results']:
            item = SteamNamesItem()
            if 'appid=570' in request.url:
                game = 'dota2'
            elif 'appid=730' in request.url:
                game = 'csgo'
            item.game = game
            item.market_hash_name = temp['asset_description']['market_hash_name']
            yield item


if __name__ == "__main__":
    SteamGetNames(redis_key="steam_get_names:filter").start()
