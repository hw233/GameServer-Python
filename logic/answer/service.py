# -*- coding: utf-8 -*-
# 活动服务
import endPoint
import answer_pb2


class cService(answer_pb2.terminal2main):
	@endPoint.result
	def rpcAnswerQuick(self, ep, who, reqMsg): return rpcAnswerQuick(who, reqMsg)

	@endPoint.result
	def rpcAnswerDay(self, ep, who, reqMsg): return rpcAnswerDay(who, reqMsg)

	@endPoint.result
	def rpcAnswerGuildHelp(self, ep, who, reqMsg): return rpcAnswerGuildHelp(who, reqMsg)

	@endPoint.result
	def rpcAnswerExtraReward(self, ep, who, reqMsg): return rpcAnswerExtraReward(who, reqMsg)

	@endPoint.result
	def rpcAnswerHelpResult(self, ep, who, reqMsg): return rpcAnswerHelpResult(who, reqMsg)

	@endPoint.result
	def rpcAnswerTreasure(self, ep, who, reqMsg): return rpcAnswerTreasure(who, reqMsg)

	@endPoint.result
	def rpcAnswerRing(self, ep, who, reqMsg): return rpcAnswerRing(who, reqMsg)

	@endPoint.result
	def rpcAnswerRingGuildHelp(self, ep, who, reqMsg): return rpcAnswerRingGuildHelp(who, reqMsg)

	@endPoint.result
	def rpcAnswerRingHelpResult(self, ep, who, reqMsg): return rpcAnswerRingHelpResult(who, reqMsg)

	@endPoint.result
	def rpcSelectFirstExam(self, ep, who, reqMsg): return answer.firstExam.rpcSelectFirstExam(who, reqMsg)

	@endPoint.result
	def rpcFirstExamClose(self, ep, who, reqMsg): return answer.firstExam.rpcFirstExamClose(who, reqMsg)
	
	@endPoint.result
	def rpcAnswerFirstExam(self, ep, who, reqMsg): return answer.firstExam.rpcAnswerFirstExam(who, reqMsg)

	@endPoint.result
	def rpcBetFlower(self, ep, who, reqMsg): return answer.betFlower.rpcBetFlower(who, reqMsg)

	@endPoint.result
	def rpcAnswerFinalExam(self, ep, who, reqMsg): return rpcAnswerFinalExam(who, reqMsg)
	
	@endPoint.result
	def rpcBetFlowerInfoReq(self, ep, who, reqMsg): return answer.betFlower.rpcBetFlowerInfoReq(who, reqMsg)
	
	@endPoint.result
	def rpcBetFlowerMainReq(self, ep, who, reqMsg): return answer.betFlower.rpcBetFlowerMainReq(who, reqMsg)


def rpcAnswerQuick(who, reqMsg):
	'''回答抢答问题
	'''
	answerQuickObj = answer.getAnswerQuickObj()
	answerQuickObj.answerProblem(who, reqMsg.sResult)

def broadcastQuickProblem(iProblemNo, duration):
	'''广播抢答题目
	'''
	msg = answer_pb2.quickProblem()
	msg.iProblemNo = iProblemNo
	msg.duration = duration
	sSerialized = endPoint.makePacket('rpcAnswerQuickProblem', msg)
	mainService.getChatEP().rpcBroadcastAnswerQuick(sSerialized)

def broadcastQuickResult(iRightOption):
	'''广播抢答答案
	'''
	msg = answer_pb2.quickResult()
	msg.iOption = iRightOption
	sSerialized = endPoint.makePacket('rpcAnswerQuickResult', msg)
	mainService.getChatEP().rpcBroadcastAnswerQuick(sSerialized)

def rpcAnswerDay(who, reqMsg):
	'''回答每日问题
	'''
	answerDayObj = answer.getAnswerDayObj()
	answerDayObj.answerProblem(who, reqMsg.sResult)

def rpcAnswerExtraReward(who, reqMsg):
	'''额外奖励翻牌
	'''
	answerDayObj = answer.getAnswerDayObj()
	answerDayObj.turnExtraReward(who, reqMsg.iValue)

def dayProblem(who, iLastOption=0):
	'''每日问题
	'''
	answerDayCnt = who.day.fetch("answerDayCnt", 0)
	lDayQuestion = who.day.fetch("answerDayQues", [])
	if len(lDayQuestion) < answerDayCnt:
		return
	iProblemNo = lDayQuestion[answerDayCnt]
	msg = {}
	msg["iProblemNo"] = iProblemNo
	
	msg["iCompleteCnt"] = answerDayCnt
	msg["iRightCnt"] = who.day.fetch("answerDayRight", 0)
	msg["iGuildHelp"] = min(3, who.day.fetch("answerGHelp", 0))
	who.endPoint.rpcAnswerDayProblem(**msg)

def rpcAnswerShowExtra(who, lAllPropsNo):
	'''显示额外奖励
	'''
	lTemp = []
	for tInfo in lAllPropsNo:
		_msg = answer_pb2.extraRewardItem()
		_msg.propsNo = tInfo[0]
		_msg.count = tInfo[1]
		lTemp.append(_msg)

	msg = answer_pb2.extraReward()
	msg.extraRewardList.extend(lTemp)
	who.endPoint.rpcAnswerShowExtra(msg)

def rpcAnswerGuildHelp(who, reqMsg):
	'''帮派求助
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你没有加入仙盟")
		return
	if who.day.fetch("answerGHelp", 0) >= 3:
		message.tips(who, '您今日求助次数已达三次，无法继续求助仙盟')
		return
	answerDayCnt = who.day.fetch("answerDayCnt", 0)
	lDayQuestion = who.day.fetch("answerDayQues", [])
	if not lDayQuestion:
		# raise Exception,"答题-每日：{}没有生成题目就答题".format(who.id)
		return
	iProblemNo = lDayQuestion[answerDayCnt]
	if not iProblemNo:
		# raise Exception,"答题-每日：{}生成题目有问题 {}|{}".format(targetRole.id, iProblemNo, lDayQuestion)
		return
	answerDayObj = answer.getAnswerDayObj()
	data = answerDayObj.getQuestionConfig(iProblemNo)
	sContent = data["题目内容"]
	content = "[求助：{}]".format(sContent)
	sLink = "#L2<{},8,0,{}>*{}*07#n".format(who.id, iProblemNo, content)
	# message.guildMessage(oGuild.id, sLink)
	message.guildRoleMessage(who.id, oGuild.id, sLink)
	iCnt = who.day.add("answerGHelp", 1)
	who.endPoint.rpcUpdateGuildHelp(iCnt)
	message.tips(who, "仙盟求助已发出")

def rpcGuildHelpHyperlink(who, targetRole, iProblemNo, *args):
	'''who帮助targetRole
	'''
	if who.id == targetRole.id:
		return
	if not iProblemNo:
		# raise Exception,"答题-每日：{}生成题目有问题 {}|{}".format(targetRole.id, iProblemNo, lOptions)
		return

	#只能答一次
	dAnswerHelpId = getattr(targetRole, "dAnswerHelpId", {})
	lHelpId = dAnswerHelpId.get(iProblemNo, [])
	if who.id in lHelpId:
		message.tips(who, "你已对该求助进行过回应了")
		return

	#已回答
	answerDayCnt = targetRole.day.fetch("answerDayCnt", 0)
	lDayQuestion = targetRole.day.fetch("answerDayQues", [])
	if iProblemNo in lDayQuestion:
		if answerDayCnt > lDayQuestion.index(iProblemNo):
			message.tips(who, '#C01{}#n已完成了该题的回答'.format(targetRole.name))
			return
	else:
		return

	msg = {}
	msg["iProblemNo"] = iProblemNo
	msg["iTargetRoleId"] = targetRole.id
	who.endPoint.rpcGuildHelpHyperlink(**msg)

def rpcAnswerHelpResult(who, reqMsg):
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你没有加入仙盟")
		return
	iTargetRoleId = reqMsg.iTargetRoleId
	iProblemNo = reqMsg.iProblemNo
	sResult = reqMsg.sResult
	targetRole = getRole(iTargetRoleId)
	if not targetRole:
		return

	#已回答
	answerDayCnt = targetRole.day.fetch("answerDayCnt", 0)
	lDayQuestion = targetRole.day.fetch("answerDayQues", [])
	if iProblemNo in lDayQuestion:
		if answerDayCnt > lDayQuestion.index(iProblemNo):
			message.tips(who, '#C01{}#n已完成了该题的回答'.format(targetRole.name))
			return

	answerDayObj = answer.getAnswerDayObj()
	data = answerDayObj.getQuestionConfig(iProblemNo)
	sContent = data["题目内容"]
	content = '我对#C01{}#n的建议是：#C02{}#n'.format(targetRole.name, sResult)
	# message.guildMessage(oGuild.id, content)
	message.guildRoleMessage(who.id, oGuild.id, content)
	message.tips(who, "答案选项提交成功！")

	message.tips(targetRole, '#C01{}#n建议你选择答案：#C02{}#n'.format(who.name, sResult))

	dAnswerHelpId = getattr(targetRole, "dAnswerHelpId", {})
	dAnswerHelpId.setdefault(iProblemNo, []).append(who.id)
	targetRole.dAnswerHelpId = dAnswerHelpId

def rpcAnswerRingGuildHelp(who, reqMsg):
	'''任务链答题求助
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你没有加入仙盟")
		return
	import task
	taskObj = task.hasTask(who, 30601)
	if taskObj:
		taskObj.askForHelp(who)

def rpcAnswerRingHelpResult(who, reqMsg):
	'''
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你没有加入仙盟")
		return
	iTargetRoleId = reqMsg.iTargetRoleId
	iProblemNo = reqMsg.iProblemNo
	sResult = reqMsg.sResult
	targetRole = getRole(iTargetRoleId)
	if not targetRole:
		return

	answerDayObj = answer.getAnswerDayObj()
	data = answerDayObj.getQuestionConfig(iProblemNo)
	sContent = data["题目内容"]
	content = '我对#C01{}#n的建议是：#C02{}#n'.format(targetRole.name, sResult)
	message.guildRoleMessage(who.id, oGuild.id, content)
	message.tips(who, "答案选项提交成功！")
	who.week.add("ringHelped", 1)
	dAnswerHelpId = getattr(targetRole, "dRingAnswerHelpId", {})
	dAnswerHelpId.setdefault(sResult, []).append(who.id)
	targetRole.dRingAnswerHelpId = dAnswerHelpId
	import task.ring
	task.ring.answerRingHelped(who, targetRole, sResult)

def rpcRingGuildHelpHyperlink(who, targetRole, iProblemNo, *args):
	'''
	'''
	if who.id == targetRole.id:
		return
	if not iProblemNo:
		return

	#只能答一次
	dAnswerHelpId = getattr(targetRole, "dRingAnswerHelpId", {})
	lHelpId = dAnswerHelpId.get(iProblemNo, [])
	if who.id in lHelpId:
		message.tips(who, "你已经回答过此题了")
		return 

	msg = {}
	msg["iProblemNo"] = iProblemNo
	msg["iTargetRoleId"] = targetRole.id
	who.endPoint.rpcRingGuildHelpHyperlink(**msg)

def rpcAnswerTreasure(who, reqMsg):
	'''回答探宝问题
	'''
	answerTreasureObj = answer.getAnswerTreasureObj()
	answerTreasureObj.answerProblem(who, reqMsg.sResult)

def treasureProblem(who, iProblemNo):
	'''探宝问题
	'''
	who.endPoint.rpcAnswerTreasureProblem(iProblemNo)

def rpcAnswerRing(who, reqMsg):
	'''回答任务链问题
	'''
	answerRingObj = answer.getAnswerRingObj()
	answerRingObj.answerProblem(who, reqMsg.sResult)

def ringProblem(who, iProblemNo, iCnt):
	'''任务链问题
	'''
	cnt = 20 + who.level / 5 - who.week.fetch("ringHelp", 0)
	who.endPoint.rpcAnswerRingProblem(iProblemNo, cnt)

#===============================================
#

def rpcFirstExamQuestion(who, iQuestionNo, iExamNo, iTime):
	'''初试问题
	'''
	msg = {}
	msg["iQuestionNo"] = iQuestionNo
	msg["iProgress"] = iExamNo
	msg["iTime"] = iTime
	who.endPoint.rpcFirstExamQuestion(**msg)


def finalExamQuestion(who):
	'''殿试问题
	'''
	lFinalExamQues = who.week.fetch("finalExamQues", [])
	answerCnt = who.week.fetch("finalExamCnt", 0)
	if len(lFinalExamQues) <= answerCnt:
		return
	iQuestionNo = lFinalExamQues[answerCnt]

	finalExamObj = answer.getAnswerFinalExamObj()

	msg = {}
	msg["iQuestionNo"] = iQuestionNo
	msg["iProgress"] = answerCnt + 1
	iErrCnt = who.week.fetch("finalExamErr", 0)
	msg["iTime"] = getSecond() - who.week.fetch("finalExamST", getSecond()) + iErrCnt*finalExamObj.errAddTime()

	who.endPoint.rpcFinalExamQuestion(**msg)

def rpcAnswerFinalExam(who, reqMsg):
	'''提交殿试答案
	'''
	finalExamObj = answer.getAnswerFinalExamObj()
	sResult = reqMsg.sValue
	finalExamObj.answerQuestion(who, sResult)


from common import *
from answer.defines import *
import answer
import mainService
import message
import openUIPanel
import answer.firstExam
import answer.betFlower
