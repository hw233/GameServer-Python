#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

IS_INNER_SERVER=True #是否内部服务器(测试服)
SHOW_EXCEPTION=True #是否将exception信息发送到客户端

ZONE_NO=1
ZONE_NAME='测试服'
PAGE_NO=1

ZONE_ID=12572	#区id(全世界唯一,无论是腾讯大区,自运营大区,美国大区,还是德国大区,彼此之间不重复)程序员硬编码时才会用到这个id

#--------路由服务配置-------------------------
ROUTE_SERVICE_IP='127.0.0.1' #路由服务ip
ROUTE_PORT_FOR_BACK_END=53001

#--------网关配置-------------------------
GATE_SERVICE_IP='127.0.0.1' #网关服务ip
GATE_PORT_FOR_GAME_CLIENT=51101 #网关端口,给游戏客户端连的
GATE_PORT_FOR_BACK_END=51201 #网关端口,给各种后端服务器连的
GATE_INSPECT_PORT=52001 #网关服务的http检查端口
GATE_BACKDOOR_PORT=52101#后门tcp端口

#--------主游戏服务起动时要临监听的端口-------------------------
MAIN_INSPECT_PORT=50201 #主服务的http检查端口
HELPER_PORT=50301 #帮助服务http端口(只在测试环境启动)
BACKDOOR_PORT=50401 #后门tcp端口
INSTRUCTION_PORT=50501 #gm服务tcp端口(供命令行客户端连接)
GM_PORT=50601 #gm服务tcp端口(供web服务器连接)

#--------场景服务起动时要临监听的端口-------------------------
SCENE_INSPECT_PORT=51301 #场景服务的http检查端口
SCENE_BACKDOOR_PORT=51701#后门tcp端口

#--------聊天服务起动时要临监听的端口-------------------------
CHAT_INSPECT_PORT=51401 #聊天服务的http检查端口
CHAT_BACKDOOR_PORT=51501 #聊天服务TCP端口

#--------游戏数据库-------------------------
MYSQL_IP_ADDRESS='127.0.0.1'
MYSQL_PORT=3306  #mysql数据库监听端口
MYSQL_USER_NAME='root'
MYSQL_PASSWORD='123456'
MYSQL_DATABASE_NAME='planb_game{}'.format(ZONE_NO) #要加上区号作为后缀,是区号不是区id,一定要用小写,断词用下划线,因为很多常用的客户端无法创建出大写库名的库(SQLyog,MySQL Workbench)

#--------中心服务配置-------------------------
CENTER_SERVICE_IP='192.168.1.130'
CENTER_PORT = 10086
CENTER_AUDIO_PORT=10087 #聊天语音http端口
CENTER_MYSQL_IP='127.0.0.1' #127.0.0.1 , 192.168.1.196
CENTER_MYSQL_PORT=3306
CENTER_DATABASE_USER_NAME='root'
CENTER_DATABASE_PASSWORD='123456'
CENTER_DATABASE_NAME='planb_center' #一定要用小写,断词用下划线,因为很多常用的客户端无法创建出大写库名的库(SQLyog,MySQL Workbench)

#用于发送创建角色,删除角色信息到登录服的数据库
LOGIN_MYSQL_IP='127.0.0.1' #127.0.0.1 , 192.168.1.196
LOGIN_MYSQL_PORT=3306
LOGIN_DATABASE_USER_NAME='root'
LOGIN_DATABASE_PASSWORD='123456'
LOGIN_DATABASE_NAME='planb_login' #一定要用小写,断词用下划线,因为很多常用的客户端无法创建出大写库名的库(SQLyog,MySQL Workbench)


#机器人
ROBOT_SERVER_IP='127.0.0.1' #'218.15.113.131'
ROBOT_SERVER_PORT=51101
ROBOT_COUNT =200  # 机器人账号数量
WALK_INTERVAL =2 # 0.1 # 走路频率，即每步多少秒
RPC_MOVE_INTERVAL = 1 # 走路发包频率，即走多少步才发移动包给服务端
