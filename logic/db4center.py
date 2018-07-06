#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import misc
import config
import mysqlCnt
#启服自动执行的sql语句,目的是方便运维
#一般是建表语句,加数据列语句,修改数据列等等各种DDL语句
#各种DDL的写法请google（Data Definition Language 数据定义语言）
#每次启服都会执行,注意不要因为重复执行毁坏结构,毁坏数据.

def init():
	global gConnectionPool
	sIp=config.CENTER_MYSQL_IP
	iPort=config.CENTER_MYSQL_PORT
	sUserName=config.CENTER_DATABASE_USER_NAME
	sPassword=config.CENTER_DATABASE_PASSWORD
	#建数据库连接池
	gConnectionPool=cConnectionPool(sIp,iPort,sUserName,sPassword,'','latin1')#暂不选定任何库
	#建数据库
	gConnectionPool.query('CREATE DATABASE IF NOT EXISTS `{}` default character set latin1'.format(config.CENTER_DATABASE_NAME))
	#选择数据库
	gConnectionPool.changeDatabase(config.CENTER_DATABASE_NAME)
	#建表
	for sSQL in gtSQL:
		if not sSQL:
			continue
		gConnectionPool.query(sSQL)

class cConnectionPool(mysqlCnt.cConnectionPool):
	INIT_CONNECTION_SIZE=1 #启动服务器时初始mysql连接个数
	MAX_CONNECTION_SIZE=7 #最多可以增加到多少个mysql连接
	#def query(self,sStatement,*tArgs):#override 
	# if config.IS_INNER_SERVER:#故意sleep的
	#	import gevent
	#	gevent.sleep(0.1)
	# return mysqlCnt.cConnectionPool.query(self,sStatement,*tArgs)
	

gtSQL=(#各个建表语句
'''
CREATE TABLE IF NOT EXISTS `role_name` (
	`roleId` bigint(20) NOT NULL,
	`pageNo` int(11) DEFAULT NULL,
	`name` varchar(100)	BINARY DEFAULT NULL,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `event_info`(  
  `eventId` BIGINT(20) NOT NULL,
  `data` LONGTEXT,
  PRIMARY KEY (`eventId`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `role_info`(  
  `roleId` BIGINT(20) NOT NULL,
  `data` LONGTEXT,
  PRIMARY KEY (`roleId`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `singleton` (
	`name` varchar(40) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `resume` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
)

import misc
import log
import config