# -*- coding: utf-8 -*-
# import answer.object
from answer.object import cAnswerBase as customActivity

giStartHour = 12
giEndHour = 24

class Activity(customActivity):
	'''答题-每日
	'''
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.needLv = 20
		self.dExtraReward = {}

	def isInTime(self):
		'''每天12:00开始直至24:00刷天前
		'''
		date = getDatePart()
		curHour = date["hour"]
		if curHour < giStartHour:
			return False
		return True

	def maxAnswerCnt(self):
		'''每天最多答题数量
		'''
		return self.getConfigInfo(1001)

	def canDayAnswer(self, who):
		'''判断是否可以答题
		'''
		if not self.isInTime():
			return '每日答题尚未开始，请您耐心等待'

		if who.level < self.needLv:
			return '您的等级不足{}级，请先加油练级'.format(self.needLv)

		if who.day.fetch("answerDayCnt", 0) >= self.maxAnswerCnt():
			return '您已回答完所有问题，请明天再来'

		return None

	def randQuestion(self, who):
		'''抽取十题
		'''
		lAllQuestion = QuestionData.gdData.keys()
		iLen = len(lAllQuestion)
		# lAllQuestion = shuffleList(lAllQuestion)
		count = self.maxAnswerCnt()
		if iLen < count:
			raise Exception,"没有可用的答题题库数据"

		lDayQuestion = []
		for i in xrange(count):
			iProblemNo = lAllQuestion[rand(len(lAllQuestion))]
			lDayQuestion.append(iProblemNo)
			lAllQuestion.remove(iProblemNo)
		who.day.set("answerDayQues", lDayQuestion)
		who.day.set("answerDayTime", getSecond())
		who.day.set("answerDayCnt", 0)
		self.answerLog("answerDay", "randQuestion {}|{}".format(who.id, lDayQuestion))
		
	def openAnswerDay(self, who, openUi=True):
		'''打开每日答题界面
		'''
		sReason = self.canDayAnswer(who)
		if sReason:
			message.tips(who, sReason)
			return
		if not who.day.fetch("answerDayQues", None):
			self.randQuestion(who)
		if openUi:
			openUIPanel.openAnswerProblem(who)
		answer.service.dayProblem(who)

	def answerProblem(self, who, sResult):
		'''回答
		'''
		sReason = self.canDayAnswer(who)
		if sReason:
			message.tips(who, sReason)
			return

		perPoint = activity.center.getPerActPoint(11)
		who.addActPoint(perPoint)
		#正在回答第几题
		answerDayCnt = who.day.fetch("answerDayCnt", 0)
		lDayQuestion = who.day.fetch("answerDayQues", [])
		if not lDayQuestion or answerDayCnt >= len(lDayQuestion):
			raise Exception,"答题-每日：{}没有生成题目就答题 {}|{}".format(who.id, answerDayCnt, lDayQuestion)
			return

		iProblemNo = lDayQuestion[answerDayCnt]
		# print "回答第%s题"%(answerDayCnt+1),iProblemNo,"提交答案:",sResult
		lAnswerResult = who.day.fetch("answerResult", [])
		if self.isRightAnswer(iProblemNo, sResult):
			# message.tips(who, '回答正确！')
			who.day.add("answerDayRight", 1)#回答题目正确数量
			lAnswerResult.append(1)
			iRewardIdx = 2001
			who.day.add("dayExmaRightN", 1)#连续正确题数
		else:
			# message.tips(who, '回答错误！')
			lAnswerResult.append(0)
			iRewardIdx = 2002
			who.day.set("dayExmaRightN", 0)#连续正确题数

		who.day.set("answerResult", lAnswerResult)
		self.answerReward(who, iRewardIdx)

		answerDayCnt = who.day.add("answerDayCnt", 1)	#回答题目数量
		activity.center.refreshTaskNpc(who)
		
		# print answerDayCnt
		if answerDayCnt >= self.maxAnswerCnt():
			#答完10题了 
			# print "答完10题了 "
			message.tips(who, '您已回答完所有问题，请明天再来')
			who.endPoint.rpcAnswerDayComplete()
			# print "rpcAnswerDayComplete"
			if who.day.fetch("answerDayRight", 0) >= 6:
				#答对的题目数大于等于6时,打开翻牌界面
				self.openExtraReward(who)
			# else:
			# 	who.endPoint.rpcAnswerDayComplete()
			return
		self.openAnswerDay(who, False)

	def answerReward(self, who, index):
		'''奖励
		'''
		# sLog = "answerReward {}|{}".format(who.id, index)
		# self.answerLog("answerDay", sLog)
		self.doScript(who, None, "R{}".format(index))

	def openExtraReward(self, who):
		'''打开额外奖励翻牌界面
		'''
		self.dExtraReward[who.id] = 1
		who.endPoint.rpcAnswerShowTurn()

	def turnExtraReward(self, who, iOption, bSendResult=True):
		'''额外奖励翻牌
		'''
		if not config.IS_INNER_SERVER:
			if who.day.fetch("answerDayRight", 0) < 6:
				return
			if who.day.fetch("answerExtra", 0):
				return
		who.day.set("answerExtra", 1)
		self.dExtraReward.pop(who.id, None)

		allData = self.getRewardPropsInfo(2001)
		idx = chooseKey(allData, key="权重")
		if idx is None:
			raise Exception,"额外奖励翻牌 idx is None"
			return
		info = allData[idx]
		if info["物品"] in ("", "0",):
			raise Exception,"额外奖励翻牌没有物品数据"
			return

		propsNo, args, kwargs = misc.parseItemInfo(info["物品"])
		amount = int(self.transCodeForReward(info["数量"], "数量", who))
		binded = info.get("绑定", 0)
		propsNo = str(self.transIdxByGroup(propsNo))
			
		if bSendResult:
			lAllPropsNo = []
			for _info in allData:
				_propsNo = _info["物品"]
				if _propsNo == propsNo:
					continue
				_count = int(self.transCodeForReward(info["数量"], "数量", who))
				lAllPropsNo.append((int(_propsNo), _count))
			shuffleList(lAllPropsNo)
			lAllPropsNo.insert(iOption-1, (int(propsNo), amount))
			lAllPropsNo = lAllPropsNo[:4]
			answer.service.rpcAnswerShowExtra(who, lAllPropsNo)
		self.launchProps(who, int(propsNo), amount, binded)

	def getValueByVarName(self, varName, who):
		if varName == "N":#连续答对的题数
			return who.day.fetch("dayExmaRightN", 0)
			# return self.continuousRightCnt(who)
		return customActivity.getValueByVarName(self, varName, who)

	def continuousRightCnt(self, who):
		'''连续答对的题数
		'''
		lAnswerResult = who.day.fetch("answerResult", [])
		cnt = 0
		for i in lAnswerResult[::-1]:
			if i == 1:
				cnt += 1
			else:
				break
		return cnt

	def directExtraReward(self, who):
		if who.id not in self.dExtraReward:
			return
		self.turnExtraReward(who, rand(1, 4), False)

	def onLogin(self, who, bRelogin):
		'''打开额外奖励翻牌重登，直接给奖励
		'''
		self.directExtraReward(who)

	def onOffline(self, who):
		'''打开额外奖励翻牌断线，直接给奖励
		'''
		self.directExtraReward(who)
		
	#==========================================
	#不弹出经验、银币的提示，但是聊天频道需要显示
	def rewardExp(self, who, val):	#override
		'''奖励角色经验
		'''
		roleId = who.id
		val = who.rewardExp(val, self.name, None)
		self.tmpReward[roleId]["经验"].append(val)
		if val > 0:
			sTips = "获得#C02$exp#n点经验"
		elif val < 0:
			sTips = "消耗#C02$exp#n点经验"
		else:
			return
		sTips = sTips.replace("$exp", str(abs(val)))
		message.message(who, sTips)

	def rewardCash(self, who, val):	#override
		'''奖励银币
		'''
		roleId = who.id
		who.rewardCash(val, self.name, None)
		self.tmpReward[roleId]["银币"].append(val)
		if val > 0:
			sTips = "获得银币#R<$cash,3,2>#n"
		elif val < 0:
			sTips = "消耗银币#R<$cash,3,2>#n"
		else:
			return
		sTips = sTips.replace("$cash", str(abs(val)))
		message.message(who, sTips)

	def rewardPetExp(self, who, val):	#override
		'''奖励宠物经验
		'''
		roleId = who.id
		petObj = who.getLastFightPet()
		self.tmpReward[roleId]["宠物经验"].append(val)
		if petObj:
			if not petObj.checkRewardExp("宠物培养", False):
				return
			petObj.addExp(val, self.name, None)
			if val > 0:
				sTips = "你的#C02$pet#n获得#C02$exp#n经验"
			elif val < 0:
				sTips = "你的$pet扣除$exp经验"
			else:
				return
			sTips = sTips.replace("$pet", petObj.name)
			sTips = sTips.replace("$exp", "%d" % abs(val))
			message.message(who, sTips)
		



from common import *
from answer.defines import *
import time
import answer
import answer.service
import log
import message
import QuestionData
import misc
import openUIPanel
import activity.center
import config
