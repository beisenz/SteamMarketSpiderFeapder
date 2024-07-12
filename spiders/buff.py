# -*- coding: utf-8 -*-
"""
Created on 2024-07-02 05:14:54
---------
@summary:
---------
@author: pc
"""

import time
import feapder
import math
from items.buff_item import BuffItem


class Buff(feapder.Spider):
    with open('secrets/buff_cookie.txt', 'r', encoding='utf-8') as file:
        BUFF_COOKIE = file.readline()

    __custom_setting__ = dict(
        SPIDER_THREAD_COUNT = 1,
        SPIDER_SLEEP_TIME = [15, 30],
    )

    def start_requests(self):
        timestamp = str(time.time() * 1000)
        timestamp = timestamp[:timestamp.index('.')]

        url = "https://buff.163.com/api/market/goods"
        for i in range(1, math.ceil(1078 / 4)):
            params = {
                "game": "csgo",
                "page_num": str(i),
                "page_size": 80,
                "sort_by": "price.desc",
                "tab": "selling",
                "use_suggestion": "0",
                "_": timestamp
            }
            yield feapder.Request(url, params=params, method="GET")

        for i in range(1, math.ceil(1193 / 4)):
            params = {
                "game": "dota2",
                "page_num": str(i),
                "page_size": 80,
                "sort_by": "price.desc",
                "tab": "selling",
                "_": timestamp
            }
            yield feapder.Request(url, params=params, method="GET")
    
    def download_midware(self, request):
        request.cookies = {
            "session": self.BUFF_COOKIE,
        }

        return request

    def parse(self, request, response):
        for temp in response.json['data']['items']:
            item = BuffItem()
            item.appid = temp.get('appid')
            item.bookmarked = temp.get('bookmarked')
            item.buy_max_price = temp.get('buy_max_price')
            item.buy_num = temp.get('buy_num')
            item.can_bargain = temp.get('can_bargain')
            item.can_search_by_tournament = temp.get('can_search_by_tournament')
            item.description = temp.get('description')
            item.game = temp.get('game')
            item.steam_price = temp.get('goods_info').get('steam_price')
            item.steam_price_cny = temp.get('goods_info').get('steam_price_cny')
            item.has_buff_price_history = temp.get('has_buff_price_history')
            item.item_id = temp.get('id')
            item.market_hash_name = temp.get('market_hash_name')
            item.market_min_price = temp.get('market_min_price')
            item.name = temp.get('name')
            item.quick_price = temp.get('quick_price')
            item.sell_min_price = temp.get('sell_min_price')
            item.sell_num = temp.get('sell_num')
            item.sell_reference_price = temp.get('sell_reference_price')
            item.short_name = temp.get('short_name')
            item.steam_market_url = temp.get('steam_market_url')
            item.transacted_num = temp.get('transacted_num')
            yield item


if __name__ == "__main__":
    Buff(redis_key="buff:filter").start()
