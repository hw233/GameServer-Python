# -*- coding: utf-8 -*-
'''答题活动相关
'''

# if 'gbOnce' not in globals():
# 	gbOnce=True
# 	if 'mainService' in SYS_ARGV:
# 		gQuestionClassify = {}
# 		gAnswerQuickObj = None	#抢答
# 		gAnswerDayObj = None	#每日
# 		gAnswerTreasureObj = None	#探宝
# 		gAnswerFirstExamObj = None	#乡试
# 		gAnswerFinalExamObj = None	#殿试
# 		gBetFlowerObj = None	#投注献花
# 		gAnswerRingObj = None


def init():
	initQuestionType()
# 	global gAnswerQuickObj
# 	gAnswerQuickObj = answer.quick.cAnswerQuick()
# 	if not gAnswerQuickObj._loadFromDB():
# 		gAnswerQuickObj._insertToDB(*gAnswerQuickObj.getPriKey())
# 	gAnswerQuickObj.init()

# 	global gAnswerDayObj
# 	gAnswerDayObj = answer.day.cAnswerDay()

# 	global gAnswerTreasureObj
# 	gAnswerTreasureObj = answer.treasure.cAnswerTreasure()

# 	global gAnswerRingObj
# 	gAnswerRingObj = answer.ring.cAnswerRing()
# 	#天问初试
# 	global gAnswerFirstExamObj
# 	gAnswerFirstExamObj = answer.firstExam.cAnswerFirstExam()
# 	if not gAnswerFirstExamObj._loadFromDB():
# 		gAnswerFirstExamObj._insertToDB(*gAnswerFirstExamObj.getPriKey())
# 	gAnswerFirstExamObj.init()


# 	#殿试
# 	global gAnswerFinalExamObj
# 	gAnswerFinalExamObj = answer.finalExam.cAnswerFinalExam()
# 	if not gAnswerFinalExamObj._loadFromDB():
# 		gAnswerFinalExamObj._insertToDB(*gAnswerFinalExamObj.getPriKey())
# 	gAnswerFinalExamObj.init()

# 	#投注献花
# 	global gBetFlowerObj
# 	gBetFlowerObj = answer.betFlower.cBetFlower()
# 	if not gBetFlowerObj._loadFromDB():
# 		gBetFlowerObj._insertToDB(*gBetFlowerObj.getPriKey())
# 	gBetFlowerObj.init()

# 	timerEvent.geNewHour += onNewHour


def getAnswerQuickObj():
	return activity.getActivity("answerQuick")
	# return gAnswerQuickObj

def getAnswerDayObj():
	return activity.getActivity("answerDay")
	# return gAnswerDayObj

def getAnswerTreasureObj():
	return activity.getActivity("treasureAnswer")
	# return gAnswerTreasureObj

def getAnswerRingObj():
	return activity.getActivity("taskRingAnswer")
	# return gAnswerRingObj

def getAnswerFirstExamObj():
	return activity.getActivity("firstExam")
	# return gAnswerFirstExamObj

def getAnswerFinalExamObj():
	return activity.getActivity("finalExam")
	# return gAnswerFinalExamObj

def getBetFlowerObj():
	return activity.getActivity("betFlower")
	# return gBetFlowerObj

# def onNewHour(year, month, day, hour, wday):
# 	'''系统刷小时
# 	'''
# 	# print "=====onNewHour===========",year, month, day, hour, wday
# 	gAnswerFirstExamObj.onNewHour(day, hour, wday)
# 	gAnswerFinalExamObj.onNewHour(day, hour, wday)

# def onLogin(who, bReLogin):
# 	'''玩家登录
# 	'''
# 	pass
	# gAnswerQuickObj.onLogin(who)
	# gAnswerFirstExamObj.onLogin(who)
	# gAnswerFinalExamObj.onLogin(who)

def initQuestionType():
	'''初始化题库类型
	'''
	global gQuestionClassify
	gQuestionClassify = {}
	for idx,info in QuestionData.gdData.iteritems():
		iType = info.get("类型", 0)
		gQuestionClassify.setdefault(iType, []).append(idx)

def getQuestionClassify(iType):
	'''获取某一类型的题库编号
	'''
	return copy.deepcopy(gQuestionClassify.get(iType, []))

import copy
# import answer.quick
# import answer.day
# import answer.treasure
# import answer.ring
# import answer.firstExam
# import answer.finalExam
# import answer.betFlower
import message
# import answer.service
# import timerEvent
import QuestionData
import activity
#===========================
#test
def testInstruction(ep, who, content, *args):
	message.tips(who, "答题指令成功")
	firstExamObj = getAnswerFirstExamObj()
	finalExamObj = getAnswerFinalExamObj()
	answerDayObj = getAnswerDayObj()
	answerQuickObj = getAnswerQuickObj()
	# print content,args
	if content == "qt":
		answerQuickObj.trigger(False)

	elif content == "sfp":
		message.tips(who, "您的献花积分为：{}".format(who.getFlowerPoint()))

	elif content == "l20r":
		rankObj = firstExamObj.dFirstExamRank[20]
		for uid in rankObj.lRanking:
			print uid,rankObj.getValue(uid)

	elif content == "der":
		answerDayObj.openExtraReward(who)
	
	elif content == "dter":
		answerDayObj.turnExtraReward(who, 1)

	#==========================================
	#初试
	elif content == "cfen":	#创建初试NPC
		firstExamObj.createFirstExamNpc()

	elif content == "dfen":	#删除初试NPC
		firstExamObj.deleteFirstExamNpc()

	elif content == "ferr":	#重置初试排行榜
		firstExamObj.resetRank()

	elif content == "thfe":	#发放金章之试参与资格
		firstExamObj.timerHandFinalExam()

	#==========================================
	#殿试
	elif content == "cfen2":	#创建殿试NPC
		finalExamObj.createFinalExamNpc()

	elif content == "dfen2":	#删除殿试NPC
		finalExamObj.deleteFinalExamNpc()

	elif content == "ferr2":	#重置殿试排行榜
		finalExamObj.resetRank()

	elif content == "fepr":	#公布殿试结果
		finalExamObj.publicResult()

	#==========================================
	#献花
	elif content == "cbfr":#清除献花记录
		who.day.delete("betFRecord")

