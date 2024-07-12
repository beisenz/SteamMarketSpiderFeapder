关于
---
- 使用Feapder框架开发，Mysql存储，Redis进行任务管理以及去重，本项目为个人测试使用，在清除其中的个人cookie数据后，遂公开代码，以方便对其Feapder开发感兴趣，或者对Steam挂刀感兴趣的朋友阅览
- 本项目初衷用于个人练习及快速开发，易用性较差，如有必要将进行优化，请详细阅读README.md
- 目前在steam挂刀方面，已有较为成熟的站点，大家自行google搜索即可，但少有对steam市集的销售单求购单、历史销售记录进行分析的，所以在之后会另起一个项目，希望可以做出点不一样的东西，如果您有任何问题或者需求，可以通过微信的方式联系我：beisenzvx

主要功能
---
- 获取BUFF平台所有商品数据，其中包含关键数据如：最低销售价格、最高求购价格、SteamMarketHashName（与Steam市场对应的数据）
- 获取Steam市场CS2、DOTA2的市集所有商品的名称数据，与获取每个商品对应销售单、求购单时所必须的item_nameid数据
- 对BUFF及STEAM分别获取后，使用Pandas将关键数据保存到excel表格

源码运行
---
1. 修改根目录下的`setting.py`，只需正确填写其中的Mysql与Redis相关信息
2. 修改secrets文件夹下的文件，该文件夹保存一些个人的Cookie与代理API，其中代理返回格式为txt，换行符为`\r\n`
3. 运行create_table文件夹下的`create_table_buff.py` `create_table_steam.py` `import_steam_names_ids_from_json.py`，请注意，在这之前你需要先配置好`setting.py`中的Mysql数据库
4. 依次运行spiders文件夹中的`buff.py`与`steam_get_graph.py`，后者依赖前者运行结束后保存的数据
5. 运行create_table文件夹中的`buff_parse.py`即可在根目录获取到包含分析后信息的`data.xlsx`文件
- 请注意，由于steam市集为海外服务器，所以获取steam市集相关数据时需要你有相应的网络环境，如果要使用代理，则需要使用原生海外网络环境的服务器运行，如果不使用代理，注释掉代理配置即可