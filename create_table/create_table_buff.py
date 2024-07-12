from feapder.db.mysqldb import MysqlDB

db = MysqlDB()

'''
buff 为 UpdateItem
market_hash_name 为 唯一索引
'''

buff_create_table_sql = """
    create table buff(
        id int primary key auto_increment,
        appid varchar(255) default null,
        bookmarked varchar(255) default null,
        buy_max_price varchar(255) default null,
        buy_num varchar(255) default null,
        can_bargain varchar(255) default null,
        can_search_by_tournament varchar(255) default null,
        description varchar(255) default null,
        game varchar(255) default null,
        steam_price varchar(255) default null,
        steam_price_cny varchar(255) default null,
        has_buff_price_history varchar(255) default null,
        item_id varchar(255) default null,
        market_hash_name varchar(255) default null,
        market_min_price varchar(255) default null,
        name varchar(255) default null,
        quick_price varchar(255) default null,
        sell_min_price varchar(255) default null,
        sell_num varchar(255) default null,
        sell_reference_price varchar(255) default null,
        short_name varchar(255) default null,
        steam_market_url varchar(255) default null,
        transacted_num varchar(255) default null,
        unique index name_index(market_hash_name)
    );
"""
db.execute(buff_create_table_sql)