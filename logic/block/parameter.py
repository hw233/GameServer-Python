# -*- coding: utf-8 -*-
import block.singleton

DEFAULT_MAX_USER_COUNT = 1500 # 默认用户上限
DEFAULT_OPEN_LEVEAL = 40 # 默认开放等级

def init():
	global parameter
	parameter = cParameter()
	if not parameter._loadFromDB():
		parameter._insertToDB(*parameter.getPriKey())


class cParameter(block.singleton.cSingleton):
	'''全局系统参数
	'''
	
	def __init__(self):
		block.singleton.cSingleton.__init__(self, "全局参数", "parameter")

	def onBorn(self):
		self.set("epochTime", timeU.getStamp())

	def load(self, data):
		if not data:
			return
		block.singleton.cSingleton.load(self, data.get("data", {}))
		
	def save(self):
		data = {}
		data["data"] = block.singleton.cSingleton.save(self)
		return data

	def getMaxUserCount(self):
		'''系统在线用户上限
		'''
		return self.fetch("maxUserCount", DEFAULT_MAX_USER_COUNT)

	def setMaxUserCount(self, count):
		'''设置系统在线用户上限
		'''
		self.set("maxUserCount", count)

	def isStaffOnly(self):
		'''是否只有公司员工可以登录游戏
		'''
		return self.fetch("staffOnly", 0)
	
	def setStaffOnly(self, val):
		'''设置是否只有公司员工可以登录游戏
		'''
		return self.set("staffOnly", val)

	def isOpenForPlayer(self):
		'''是否允许玩家登录
		'''
		return self.fetch("openForPlayer", 1)

	def setOpenForPlayer(self, val):
		'''设置是否允许玩家登录
		'''
		self.set("openForPlayer", val)

	def getEpochTime(self):
		'''字符串,开新服的时间(开区时开始计)
		'''
		return timeU.stamp2str(self.fetch("epochTime"))
	
	def getOpenLevel(self):
		'''开放等级
		'''
		return self.fetch("openLevel", DEFAULT_OPEN_LEVEAL)
	
	def setOpenLevel(self, level):
		'''设置开放等级
		'''
		self.set("openLevel", level)
	
	def getOpenDay(self):
		'''开放天数
		'''
	   	return self.fetch("openDay")

	def setOpenDay(self, day):
		'''设置开放天数
		'''
	  	self.set("openDay", day)

import u
import misc
import timeU
