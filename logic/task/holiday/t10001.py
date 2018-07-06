# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	parentId = 10001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''节日礼物领取'''
	intro = '''与$target说话'''
	detail = '''$holiday到了，$target要送你一个大礼包，快过去看看吧！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10206,1001)'''

	npcInfo = {
	}

	eventInfo = {
		1001:{"点击":"LOOK"},
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
		2013:'''$holiday已经过去了,下个节日也有大礼哦''',
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}

	lineupInfo = {
	}

	configInfo = {
		"生成路径":"holiday",
	}
#导表结束

	def canAbort(self):
		'''是否可以放弃任务
		'''
		return 0

	def onBorn(self, who, npcObj, **kwargs):
		'''出生时初始化，只在给予任务时执行一次
		'''
		holidayId = holidayData.getCurrentHoliday()
		self.set("holidayId",holidayId)
		customTask.onBorn(self, who, npcObj, **kwargs)

	def transString(self, content, pid=0):
		'''转化字符串
		'''
		holidayId = self.fetch("holidayId")
		holidayName = holidayData.getConfig(holidayId,"节日名称")
		content = content.replace("$holiday", holidayName)

		return customTask.transString(self, content, pid)

	def isValid(self):
		'''是否有效
		'''
		holidayId = holidayData.getCurrentHoliday()
		if not holidayId or not self.fetch("holidayId"):
			return 0
		if holidayId != self.fetch("holidayId"):
			self.set("holidayId",holidayId)

		return customTask.isValid(self)

	@property	
	def rewardDesc(self):
		'''奖励描述
		'''
		holidayId = self.fetch("holidayId")
		reward = holidayData.getConfig(holidayId,"奖励").keys()
		return ",".join([str(i) for i in reward])

	def goAhead(self, who):
		'''前往
		'''
		if not holidayData.getCurrentHoliday():
			self.doScript(who, None, "TP2013")
			task.removeTask(who,self.id)
			return

		customTask.goAhead(self, who)

	def onNewDay(self):
		'''刷天
		'''
		holidayId = holidayData.getCurrentHoliday()
		if not holidayId or holidayId == self.fetch("holidayId"):
			return
		self.set("holidayId",holidayId)
		who = getRole(self.ownerId)
		if who:
			task.service.rpcTaskChange(who,self,"detail","rewardDesc","title")


from common import *
import re
import holidayData
import template
import task
import task.service
