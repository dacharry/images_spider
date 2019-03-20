# spider_pratice
## 几个网站的爬取练习
## bmw
- 第一个基本spider爬取汽车之家宝马5系的缩略图
- 第二个crawlspider爬去汽车之家宝马5系的高清图
## jianshu_spider
- 爬去的简书文章信息，并保存在mysql
- 利用selenium加载动态网页，在middleware中返回response。
## boss
- boss直聘网站关于python的爬去
- 用代理ip来解决ip封禁问题

## amazon和amazo_redis
- 爬去amazon的所有图书的信息，包括价格，名字，作者，评论数等
- 一个是crawlspider，一个是rediscrawlspider分布式爬去
- 难点在于电子书与纸质书的标签是不一样的，还有就是提取出合适的数据



## MaiTian
- 爬去麦田北京二手房信息，包括每平方价格，区域，名称，其他信息
- 在下载中间件使用随机user-agent
- 随机ip，先运行get_proxy.py得到5个代理ip，再在中间件中建立一个列表，随机从列表取出ip，最后在爬去46页后被封
