#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import mysqlCnt
#启服自动执行的sql语句,目的是方便运维
#一般是建表语句,加数据列语句,修改数据列等等各种DDL语句
#各种DDL的写法请google（Data Definition Language 数据定义语言）
#每次启服都会执行,注意不要因为重复执行毁坏结构,毁坏数据.

def init():
	global gConnectionPool
	sIp,iPort=config.LOGIN_MYSQL_IP,config.LOGIN_MYSQL_PORT
	sUserName,sPassword=config.LOGIN_DATABASE_USER_NAME,config.LOGIN_DATABASE_PASSWORD
	sDatabaseName=config.LOGIN_DATABASE_NAME
	#建数据库连接池
	gConnectionPool=cConnectionPool(sIp,iPort,sUserName,sPassword)#暂不选定任何库
	#建数据库
	#gConnectionPool.query('CREATE DATABASE IF NOT EXISTS `{}`'.format(sDatabaseName))
	#选择数据库
	gConnectionPool.changeDatabase(sDatabaseName)
	#建表
	for sSQL in gtSQL:
		if not sSQL:
			continue
		gConnectionPool.query(sSQL)

class cConnectionPool(mysqlCnt.cConnectionPool):
	INIT_CONNECTION_SIZE=1 #启动服务器时初始mysql连接个数
	MAX_CONNECTION_SIZE=2 #最多可以增加到多少个mysql连接
	#def query(self,sStatement,*tArgs):#override 
	#	if config.IS_INNER_SERVER:#故意sleep的
	#		import gevent
	#		gevent.sleep(0.1)
	#	return mysqlCnt.cConnectionPool.query(self,sStatement,*tArgs)
	

gtSQL=(#各个建表语句
)


#注意事项：sql关键字请用大写,不要用select这样的小写,大写sublime text编辑器可以语法高亮
#用于登录界面的"拥有角色""
CREATE_ROLE='INSERT INTO role (roleId,zoneNo,userSource,account) VALUES({},{},"{}","{}")'
DELETE_ROLE='DELETE FROM role WHERE roleId={}'

import config
