#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#id生成器
#公会id,玩家id.....都以服务器编号作为后缀,保证真正的唯一,合区时也不冲突
class cGUIdGenerator(object):
	def __init__(self,sSql):
		self.iNextId=0
		self.sSql=sSql

	def loadFromDB(self):
		iDecCarry=u.decimalCarry(config.ZONE_NO)
		iMod=10**(iDecCarry+1)
		iIdPostfix=config.ZONE_NO*10+iDecCarry
		rs=db4ms.gConnectionPool.query(self.sSql,iMod,iIdPostfix)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:
			raise Exception,'肯定有1行,即使是表里没有数据,因为sql语句使用了max聚合函数'
		if len(rs.rows[0])!=1:
			raise Exception,'列数只能是1列'
		i=rs.rows[0][0]

		if not i:#数据库的null会表现为python的None
			self.iNextId=u.guIdWithPostfix(config.ZONE_NO)
		else:
			self.iNextId=u.guIdWithPostfix(config.ZONE_NO,i,True)

	def nextId(self):
		if self.iNextId==0:
			raise Exception,'请先调用loadFromDB进行初始化'
		i=self.iNextId
		self.iNextId=u.guIdWithPostfix(config.ZONE_NO,self.iNextId,True)
		return i

#角色id生成器
class cRoleIdGenerator(cGUIdGenerator):
	def nextId(self):#override
		iRoleId=cGUIdGenerator.nextId(self)
		if iRoleId>c.MAX_ROLE_ID:
			raise Exception,'角色id已用完,id={}'.format(iRoleId)
		return iRoleId


def init():
	global gRoleId,gGuildId
	gRoleId=cRoleIdGenerator(sql.MAX_ROLE_ID)#角色id生成器
	gGuildId=cGUIdGenerator(sql.MAX_GUILD_ID)#公会id生成器

	gRoleId.loadFromDB()
	gGuildId.loadFromDB()

import misc
import config
import sql
import db4ms
import u
import c
import log