# -*- coding: utf-8 -*-
'''
系统设置相关
'''
	
def testtime(ep, year, month, day, hour=0, minute=0, sec=0):
	'''设置测试时间
	'''
	if not IS_INNER_SERVER:
		return
	if not vaildTime(year, month, day, hour, minute, sec):
		ep.rpcTips("设置测试时间异常，设置失败")
		return

	ti = int(time.time())
	seconds = time.mktime((year, month, day, hour, minute, sec, 0, 0, 0))
	timerEvent.gTempTime = int(seconds) - ti
	ep.rpcTips("设置测试时间为：%d年%d月%d日 %02d:%02d" % (year, month, day, hour, minute))
	
def vaildTime(year, month, day, hour, minute, sec):
	if year < 1970 or year > 2037:
		return False
	if month < 1 or month > 12:
		return False
	if day < 1 or day > 31:
		return False
	if hour < 0 or hour > 24:
		return False
	if minute < 0 or minute > 60:
		return False
	if sec < 0 or sec > 60:
		return False
	return True

def resettime(ep):
	'''重置时间
	'''
	if not IS_INNER_SERVER:
		return
	timerEvent.gTempTime = None
	ep.rpcTips("成功重置时间")

def newhour(ep):
	'''刷时
	'''
	if not IS_INNER_SERVER:
		return
	ep.rpcTips("ok")
	timerEvent.onNewHour()

def newday(ep):
	'''刷天
	'''
	if not IS_INNER_SERVER:
		return
	ep.rpcTips("ok")
	timerEvent.gDayNo -= 1
	timerEvent.onNewHour()
	
def newweek(ep):
	'''刷周
	'''
	if not IS_INNER_SERVER:
		return
	ep.rpcTips("ok")
	timerEvent.gWeekNo -= 1
	timerEvent.onNewHour()
	
def newmonth(ep):
	'''刷月
	'''
	if not IS_INNER_SERVER:
		return
	ep.rpcTips("ok")
	timerEvent.gMonthNo -= 1
	timerEvent.onNewHour()
	
def setMaxUserCount(ep, count):  # 设置服务器最高在线人数
	countOld = block.parameter.parameter.getMaxUserCount()
	block.parameter.parameter.setMaxUserCount(count)
	ep.rpcTips('最高人数上限由{}改为{}'.format(countOld, count))
	

def openLevelMsg(ep):
	'''服务器开放等级信息
	'''
	txtList = []
	txtList.append("当前服务器等级:%d" % openLevel.getOpenLevel())
	txtList.append("%d天后开启新等级" % openLevel.getOpenDay())
	who = getRole(ep.iRoleId)
	message.dialog(who, "\n".join(txtList))

def setOpenLevel(ep,level):
	'''设置服务器开放等级
	'''
	block.parameter.parameter.setOpenLevel(level)
	openLevel.updateToPlayer()
	ep.rpcTips("设置成功")

def setOpenDay(ep,day):
	'''设置服务器开放时间
	'''
	block.parameter.parameter.setOpenDay(day+getDayNo())
	ep.rpcTips("设置成功")

def openLevelNow(ep):
	'''立刻开放服务器新等级
	'''
	parameter = block.parameter.parameter
	level = parameter.getOpenLevel()
	newLevel = openLevelData.getConfig(level,"开启等级") + level

	parameter.setOpenLevel(newLevel)
	parameter.setOpenDay(0)
	openLevel.updateToPlayer()

	ep.rpcTips("服务器新等级开放成功")

from common import *
from config import *
import time
import timerEvent
import block.parameter
import message
import openLevelData
import openLevel