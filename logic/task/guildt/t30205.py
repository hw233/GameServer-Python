# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''仙盟-小惩大诫'''
	intro = '''前往教训出言不逊的$target'''
	detail = '''听闻$target在外编造我们仙盟坏话，你去教训一下$target。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NE(9003,1004)'''
#导表结束

	def createNpc(self, npcIdx, who=None):#override
		'''创建Npc
		'''
		npcObj = customTask.createNpc(self, npcIdx, who)
		targetId = 0
		# 设置从排行榜拉出来的数据：名称，造型，染色
		guildObj = who.getGuildObj()
		actObj = activity.guildFight.getActivity()
		signUpObj = actObj.signUpList.get(guildObj.id)
		if signUpObj:
			pkGuildObj = signUpObj.getPKGuildObj()
			if pkGuildObj:
				memberList = copy.copy(pkGuildObj.memberList)
				if memberList:
					targetId = shuffleList(memberList, 1)[0]
		if not targetId:
			rankObj = rank.getRankObjByName("rank_school_all") #总榜
			ranking = copy.copy(rankObj.lRanking[:50])
			if who.id in ranking:
				ranking.remove(who.id)
			if ranking:
				targetId = shuffleList(ranking, 1)[0]
		if targetId:
			resumeObj = resume.getResume(targetId)
			npcObj.name = resumeObj.fetch("name")
			npcObj.shape = resumeObj.fetch("shape")
			shapeParts = resumeObj.fetch("shapeParts")
			if shapeParts:
				npcObj.shapeParts = shapeParts
			npcObj.school = resumeObj.fetch("school")
		return npcObj
	
	def onMissionDone(self, who, npcObj):
		pass


import copy
from common import *
import myGreenlet
import task
import rank
import activity.guildFight
import resume
