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
	sIp=config.MYSQL_IP_ADDRESS
	iPort=config.MYSQL_PORT
	sUserName=config.MYSQL_USER_NAME
	sPassword=config.MYSQL_PASSWORD
	#建数据库连接池
	gConnectionPool=cConnectionPool(sIp,iPort,sUserName,sPassword,'','latin1')#暂不选定任何库
	#建数据库
	gConnectionPool.query('CREATE DATABASE IF NOT EXISTS `{}` default character set latin1'.format(config.MYSQL_DATABASE_NAME))
	#选择数据库
	gConnectionPool.changeDatabase(config.MYSQL_DATABASE_NAME)
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
CREATE TABLE IF NOT EXISTS `account_json` (
	`userSource` varchar(20) NOT NULL,
	`account` varchar(40) BINARY NOT NULL,
	`data` longtext,
	PRIMARY KEY (`userSource`,`account`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `account_multi_field` (
	`userSource` varchar(20) NOT NULL,
	`account` varchar(40)	BINARY NOT NULL,
	`diamond` int(11) DEFAULT NULL,
	`vipLv` int(11) DEFAULT NULL,
	`vipExp` int(11) DEFAULT NULL,
	`createTime` datetime NOT NULL,
	PRIMARY KEY (`userSource`,`account`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `cycle` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `friend` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `fruition` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `guild` (
	`guildId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`guildId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `house` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `mail` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `gold_coin` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `active` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `lazy` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `pet` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `props` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='包裹';
''',
'''
CREATE TABLE IF NOT EXISTS `equip` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='装备';
''',
'''
CREATE TABLE IF NOT EXISTS `resume` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `role_multi_field1` (
	`roleId` bigint(20) NOT NULL,
	`userSource` varchar(20) DEFAULT NULL,
	`account` varchar(40) BINARY DEFAULT NULL,
	`name` varchar(100)	BINARY DEFAULT NULL,
	`exp` bigint(20) NOT NULL DEFAULT '0',
	`pro` tinyint(4) DEFAULT NULL,
	`wp` int(11) DEFAULT 1,
	`lv` int(11) NOT NULL DEFAULT '0',
	`gold` bigint(20) NOT NULL DEFAULT '0',
	`leagueRank` int(11) NOT NULL DEFAULT '0',
	`createTime` datetime NOT NULL,
	`delTime` datetime DEFAULT NULL,
	`registerAppId` varchar(20) DEFAULT NULL,
	`status` tinyint(1) DEFAULT '0',
	`banToTime` datetime DEFAULT NULL COMMENT '禁止登录截止时间',
	`banReason` varchar(256) DEFAULT NULL,
	`arenaPoint` bigint(20) NOT NULL DEFAULT '0',
	`voucher` bigint(20) NOT NULL DEFAULT '0',
	`loginTime` datetime DEFAULT NULL,
	`logoutTime` datetime DEFAULT NULL,
	PRIMARY KEY (`roleId`),
	UNIQUE KEY `uniqueName` (`name`),
	INDEX `league` (`leagueRank`),
	INDEX `roleList` (`account`,`userSource`,`status`)	
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `singleton` (
	`name` varchar(40) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `skill` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `task` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `title` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `buff` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `pet` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `buddy` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `activity` (
	`activityId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`activityId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `lineup` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `storage` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `numen_bag` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `state` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `words` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `offline` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `eye` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `achv` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
'''
CREATE TABLE IF NOT EXISTS `ride` (
	`roleId` bigint(20) NOT NULL,
	`data` longtext,
	PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
''',
)

import misc
import log
import config