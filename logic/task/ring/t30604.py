# -*- coding: utf-8 -*-
from task.defines import *
from task.ring.t30601 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30601
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''入世修行'''
	intro = '''据闻高手$target在附近出没，去请教一番'''
	detail = '''遇见高手，岂可置若罔闻。前往领教$target的武艺。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NE(1001,1005)'''
#导表结束

	def createNpc(self, npcIdx, who=None):#override
		'''创建Npc
		'''
		npcObj = customTask.createNpc(self, npcIdx, who)
		# 设置从排行榜拉出来的数据：名称，造型，染色
		rankObj = rank.getRankObjByName("rank_school_all") #总榜
		ranking = copy.copy(rankObj.lRanking)
		if who and who.id in ranking:
			ranking.remove(who.id)
		if ranking:
			targetId = shuffleList(ranking, 1)[0]
			resumeObj = resume.getResume(targetId)
			npcObj.name = resumeObj.fetch("name")
			npcObj.shape = resumeObj.fetch("shape")
			shapeParts = resumeObj.fetch("shapeParts")
			if shapeParts:
				npcObj.shapeParts = shapeParts
			npcObj.school = resumeObj.fetch("school")
		return npcObj

	def transAbleInfo(self, who, fightIdx, ableInfo, npcObj=None):
		'''转化怪物能力表数据
		'''
		result = {}
		# 难度系数 = 90% + (int(环数/10)-5)*4% + random(0,5)%
		sDif = self.configInfo.get(5002, "90").replace("R", str(self.getRing(who)))
		difficulty = getattr(self, "difficulty", None)
		if not difficulty:
			self.difficulty = eval(sDif) * 0.01
		for _type, code in ableInfo.iteritems():
			code = self.transCodeForFight(code, _type, who)
			if isinstance(code, str):
				code = code.replace("B", "B*{:.2f}".format(self.difficulty))
			result[_type] = code
		return result

	def warWin(self, warObj, npcObj, warriorList):
		'''战斗胜利
		'''
		ownerId = self.ownerId
		ownerObj = getRole(ownerId)
		guildId = ownerObj.getGuildId()
		sHelpExp = self.configInfo.get(1002, "1000")
		helpPt = self.configInfo.get(1003, 2) # 侠义
		helpPtE = self.configInfo.get(1004, 1) # 同仙盟额外侠义
		sFightHelpCnt = self.configInfo.get(5005, "1") # 战斗帮助次数
		ownerObj.week.add("ringHelp2", 1)
		for w in warriorList:
			if not w.isRole():
				continue
			who = getRole(w.id)
			if not who:
				continue
			if not self.inGame(who) or who.id != ownerId:
				exp = eval(sHelpExp.replace("LV", str(who.level)))
				helpP = helpPt
				helped = who.week.add("ringHelped2", 1)
				surplus = eval(sFightHelpCnt.replace("LV", str(who.level))) - helped
				if guildId and who.getGuildId() == guildId:
					helpP += helpPtE
				message.message(who, "帮助完成入世修行求助，获得经验#C02{}#n，侠义值#R<{},6,2>#n，本周剩余可帮助次数{}".format(exp, helpP, surplus))
				who.rewardExp(exp, "帮助任务链战斗", None)
				who.addHelpPoint(helpP, "帮助任务链战斗", None)
				continue
			self.onWarWin(warObj, npcObj, w)

	def getHyperLink(self, who):
		'''获取任务求助超链接
		'''
		if who.inTeam() and not who.getTeamObj().isLeader(who.id):
			message.tips(who, "队员状态无法发送入世修行战斗求助链接")
			return None
		npcObj = self.getTargetNpc()
		iRing = self.getRing(who)
		sLink = "#L2<{},3,{},{}>*[申请加入]*08#n".format(who.id, self.getUniqueId(), self.id)
		content = "我在{}环#L1<14,20>*[入世修行]*02#n中遇到强敌#C01{}#n，请求帮助{}".format(iRing, npcObj.name, sLink)
		team.makeTeam(who)
		message.tips(who, "发送入世修行战斗求助链接，自动开启组队")
		return content

	def askForHelp(self, who):
		'''求助
		'''
		oGuild = who.getGuildObj()
		if not oGuild:
			message.tips(who, "您没有加入帮派")
			return
		sHelpCnt = self.configInfo.get(5003, "20")
		helpCnt = eval(sHelpCnt.replace("LV", str(who.level)))
		if who.week.fetch("ringHelp2", 0) >= helpCnt:
			message.tips(who, "入世修行求助次数不足，请等待下周或提升等级后再次尝试")
			return
		sLink = self.getHyperLink(who)
		if not sLink:
			return
		message.guildRoleMessage(who.id, oGuild.id, sLink)
		message.tips(who, "帮派求助已发出")

	def offerHelp(self, who):
		'''提供帮助
		'''
		if who.inEscort() or who.inTreasure():
			message.tips(who, "当前状态下不能进行此类操作")
			return
		sFightHelpCnt = self.configInfo.get(5005, "1") # 战斗帮助次数
		cnt = eval(sFightHelpCnt.replace("LV", str(who.level)))
		if who.week.fetch("ringHelped2") >= cnt:
			message.tips(who, "本周战斗帮助次数已达上限")
			return
		msg = team_pb2.member()
		msg.roleId = self.ownerId
		team.service.rpcTeamApplyJoin(who, msg)

	def customEvent(self, who, npcObj, eventName, *args):
		m = re.match("check(\S+)", eventName)
		if m:
			subEvent = m.group(1)
			myGreenlet.cGreenlet.spawn(self.handleCheck, who.id, npcObj.id, subEvent)

	def handleCheck(self, pid, npcId, eventName):
		who = getRole(pid)
		if not who:
			return
		npcObj = getNpc(npcId)
		if not npcObj:
			return
		school = npcObj.school
		groupId = 9000 + school % 10
		self.doScript(who, npcObj, "F{}".format(groupId))



from common import *
import resume
import rank
import copy
import message
import team
import team.service
import team_pb2
import myGreenlet
