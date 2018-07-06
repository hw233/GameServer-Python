# -*- coding: utf-8 -*-
'''
称号
'''
import pst

class cTitle(pst.cEasyPersist):
	def __init__(self, iNo):
		pst.cEasyPersist.__init__(self)
		self.iNo = iNo
		self.id = iNo
		self.iOwnerId = 0
		self.iBirthday = 0

	def onBorn(self, who, **dArgs):#override
		self.iBirthday=int(time.time())#激活时间
		self.set("bd", self.iBirthday)

		iEndTime = dArgs.get("et", 0)	#失效时间
		if iEndTime:
			self.set("et", iEndTime)

	@property
	def key(self):
		return self.iNo

	@property
	def name(self):
		cfgName = self.getConfig("称谓名称")
		if self.groupId == 20101:
			who = self.getOwnerObj()
			if not who:
				return cfgName
			guildName = who.getGuildName()
			return guildName + cfgName
		return cfgName

	@property
	def groupId(self):
		return self.getConfig("组编号")

	@property
	def groupIdx(self):
		return self.getConfig("组系数")

	@property
	def pathLink(self):
		return self.getConfig("获取途径链接")

	@property
	def titleEffect(self):
		return self.getConfig("称谓特效")

	def load(self,dData):#override
		pst.cEasyPersist.load(self, dData)
		self.iBirthday=self.fetch("bd")

	def getBirthday(self):
		return self.iBirthday

	def getExpire(self):
		'''获取过期时间(UTC秒)
		'''
		iEndTime = self.fetch("et")
		if iEndTime:
			return iEndTime - getSecond()
		expire = self.getConfig("有效期")
		if expire < 0: ##永远有效
			return None
		iLen = len(expire)
		if iLen == 2:
			iLast = (24 * expire[0] + expire[1]) * 3600
			return iLast + self.iBirthday - getSecond()
		elif iLen == 3:
			return int(time.mktime((expire[0],expire[1],expire[2],0,0,0,0,0,0))) - getSecond()

	def isActive(self):
		'''是否有效
		'''
		iEndTime = self.fetch("et")
		if iEndTime:
			return iEndTime > getSecond()
		expire = self.getConfig("有效期")
		if expire < 0: ##永远有效
			return True 
		if not isinstance(expire, tuple):
			return False
		iLen = len(expire)
		if iLen == 2:
			iLast = (24 * expire[0] + expire[1]) * 3600
			return iLast + self.iBirthday > getSecond()
		elif iLen == 3:
			return int(time.mktime((expire[0],expire[1],expire[2],0,0,0,0,0,0))) > getSecond()
		return False

	def timeOut(self):
		'''超时
		'''
		if hasattr(self, "timerMgr") and self.timerMgr.hasTimerId("timeOut"):
			self.timerMgr.cancel("timeOut")
			self.timerMgr = None
		who = self.getOwnerObj()
		if not who:
			return
		who.titleCtn.removeTitle(self)
		who.reCalcAttr()#重新计算人物属性
		writeLog("title/remove", "%d title %d timeout removed" % (who.id, self.key))
		message.tips(who, "称谓#C02{}#n已到期".format(self.name))

	def getConfig(self, sKey, uDefault=0):
		return titleData.getConfig(self.iNo,sKey,uDefault)

	def transEffect(self):
		effect = self.getConfig("效果")
		if not effect:
			return {}
		dEffect = {}
		for data in effect.split(","):
			k, v = data.split(":")
			dEffect.update({k:v})
		return dEffect

	def getEffect(self):
		'''效果，把配表的原始数据生成处理一下，方便调用
		'''
		if not hasattr(self,"effect"):
			self.effect = {}
			dAttrCh2En = role.defines.descAttrList
			for sKey,uValue in self.transEffect().iteritems():
				sKey = dAttrCh2En[sKey]#故意不抛错，方便前期测试
				self.effect[sKey] = eval(uValue)
		return self.effect

	@property
	def ownerId(self):
		return self.iOwnerId

	@ownerId.setter
	def ownerId(self, ownerId):
		self.iOwnerId = ownerId

	def getOwnerObj(self):
		return getRole(self.ownerId)

	def setup(self, who, isLogin=False):
		if not self.isActive():
			return
		ti = self.getExpire()
		if ti != None:
			if ti > 0:
				self.timerMgr = timer.cTimerMng()
				self.timerMgr.run(self.timeOut, ti, 0, "timeOut")
			else:
				self.timeOut()
				return
		sFlag = 'title{}'.format(self.key)
		for sKey,iValue in self.getEffect().iteritems():
			who.addApply(sKey,iValue,sFlag)

	def cancelSetup(self, who):
		who.removeApplyByFlag('title{}'.format(self.key))


import time
import timer
import role.defines
import titleData
from common import *
import message
