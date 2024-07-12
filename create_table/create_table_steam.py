from feapder.db.mysqldb import MysqlDB

db = MysqlDB()

'''
steam_names steam_names_ids 为 Item
steam_graph 为 UpdateItem market_hash_name 为唯一索引
'''

steam_names_create_table_sql = """
    create table steam_names(
        id int primary key auto_increment,
        game varchar(255) default null,
        market_hash_name varchar(255) default null
    );
"""
db.execute(steam_names_create_table_sql)

steam_names_ids_create_table_sql = """
    create table steam_names_ids(
        id int primary key auto_increment,
        game varchar(255) default null,
        market_hash_name varchar(255) default null,
        item_nameid varchar(255) default null
    );
"""
db.execute(steam_names_ids_create_table_sql)

steam_graph_create_talble_sql = """
    create table steam_graph(
        id int primary key auto_increment,
        item_nameid varchar(255) default null,
        market_hash_name varchar(255) default null,
        buy_order_graph TEXT default null,
        sell_order_graph TEXT default null,
        unique index name_index(market_hash_name)
    );
"""
db.execute(steam_graph_create_talble_sql)