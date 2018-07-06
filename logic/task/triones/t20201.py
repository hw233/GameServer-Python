# -*- coding: utf-8 -*-
from task.defines import *
from task.object import Task as customTask

#导表开始
class Task(customTask):
	parentId = 20201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''北斗七星'''
	intro = '''战胜$monsterList'''
	detail = '''北斗七星下凡，去战胜$monsterList。在$allScene有可能找到北斗七星。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''

	npcInfo = {
	}

	eventInfo = {
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
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
		"生成路径":"triones",
	}
#导表结束

	def onBorn(self, who, npcObj, **kwargs):#override
		'''
		'''
		customTask.onBorn(self, who, npcObj, **kwargs)
		#定时
		datePart = getDatePart()
		lEndTime = []
		lEndTime.append(datePart["year"])	#年
		lEndTime.append(datePart["month"])	#月
		lEndTime.append(datePart["day"]+1)	#日
		lEndTime.append(0)					#时
		lEndTime.append(0)					#分
		lEndTime.append(0)					#秒

		iEndTime = getSecond(*lEndTime)
		leftTime = iEndTime - getSecond()
		self.setTime(leftTime) # 计时任务


	def canAbort(self):
		'''是否可以放弃任务
		'''
		return 0

	def isValid(self):
		'''是否有效
		'''
		actObj = activity.triones.getActivity()
		if actObj:
			if actObj.inNormalTime():
				return 1
			else:
				return 0
		return customTask.isValid(self)

	def goAhead(self, who):
		'''前往:任务点击无法寻路
		'''
		actObj = activity.triones.getActivity()
		ti = self.getTime()
		if ti < 0:
			self.timeOut()
			message.tips(who, actObj.getText(6003))
			return
		message.tips(who, actObj.getText(4012))

	def transString(self, content, pid=0):#override
		'''转化字符串
		'''
		if "$monsterList" in content or "$allScene" in content:
			actObj = activity.triones.getActivity()
			if actObj:
				if "$monsterList" in content:
					lKillMonster = []
					lTemp = []
					who = None
					if pid:
						who = getRole(pid)
					if who:
						lKillMonster = who.day.fetch("trionesKill", [])
					#未战胜显示#C04
					#已战胜显示#C05
					for monsterIdx in xrange(1001, 1008):
						info = actObj.getNpcInfo(monsterIdx)
						if monsterIdx in lKillMonster:
							lTemp.append("#C0{}{}#n".format(5, info.get("名称", "")))
						else:
							lTemp.append("#C0{}{}#n".format(4, info.get("名称", "")))

					content = content.replace("$monsterList", "、".join(lTemp))

				if "$allScene" in content:
					lTemp = []
					lAllScene = actObj.getGroupInfo(9001)
					for iSceneId in lAllScene:
						sceneObj = scene.getScene(iSceneId)
						if sceneObj:
							lTemp.append("#C08{}#n".format(sceneObj.name))

					content = content.replace("$allScene", "、".join(lTemp))

		return customTask.transString(self, content, pid)



from common import *
import message
import activity.triones
import scene

	