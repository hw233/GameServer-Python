# -*- coding: utf-8 -*-
# import answer.object
# import block.singleton
from answer.object import cAnswerBase as customActivity
from activity.object import Npc as customNpc

class Activity(customActivity):
	'''答题-金章之试（殿试）
	'''
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.week=cycleData.cCycWeek(2, self.markDirty)
		self.timerMgr = timer.cTimerMng()
		self.finalExamNpcObj = None
		self.reset()

	def reset(self):
		'''重置
		'''
		pass

	def init(self):
		#起服在答题期间，创建NPC
		if self.isShowNpcTime():
			self.createFinalExamNpc()
		#设置结束定时器
		self.setEndTimer()

	def load(self,dData):#override
		customActivity.load(self, dData)
		self.week.load(dData.pop('w',{}))

	def save(self):#override
		dData = customActivity.save(self)
		dHour=self.week.save()
		if dHour:
			dData['w']=dHour
		return dData

	def maxAnswerCnt(self):
		'''最多答题数量
		'''
		return self.getConfigInfo(2002)

	def setFinalExamRoleId(self, lRoleId):
		'''设置金章之试参与资格
		'''
		self.week.set("finalExamId", lRoleId)

	def hasQualifications(self, pid):
		'''是否有资格考试
		'''
		if gbNotLimitTime:
			return True
		lFinalExamId = self.week.fetch("finalExamId", [])
		return pid in lFinalExamId

	def getFinalExamList(self):
		'''入围名单
		'''
		return self.week.fetch("finalExamId", [])

	def isShowNpcTime(self):
		'''显示NPC时间 周六12:00-24:00
		'''
		if gbNotLimitTime:
			return True
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		if curHour < 12:
			return False
		return True

	def isInAnswerTime(self):
		'''答题时间周六21:00-22:00
		'''
		if gbNotLimitTime:
			return True
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		if curHour < 21 or curHour >= 22:
			return False
		return True

	def isAnswerEndFiveMin(self):
		'''22:00-22:05
		'''
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		curMinute = date["minute"]
		if curHour == 22 and curMinute <= 5 :
			return True
		return False

	def isAnswerEnd(self):
		'''22:05后
		'''
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return False
		curHour = date["hour"]
		curMinute = date["minute"]
		if curHour >= 22 and curMinute > 5 :
			return True
		return False

	def onNewHour(self, day, hour, wday):
		'''系统刷小时
		'''
		date = getDatePart()
		wday = date["wday"]
		curHour = date["hour"]
		#星期日0点删除NPC
		if wday == 7 and curHour == 0:	
			self.deleteFinalExamNpc()

		if wday != 6:
			return

		# if curHour == 0:	#星期六0点重置排行榜
		# 	self.resetRank()

		if curHour == 12:		#创建NPC
			# self.resetRank()	#再次清空排行榜，怕错过了
			self.reset()
			self.createFinalExamNpc()

		elif curHour == 21:		#创建NPC
			if not self.finalExamNpcObj:
				self.createFinalExamNpc()

		elif curHour == 22:		#设置定时器，22:30公布结果
			self.setEndTimer()


	def createFinalExamNpc(self):
		'''创建NPC放入场景
		'''
		self.deleteFinalExamNpc()
		npcObj = self.addNpc(1021, "finalExam")#self.addWeekAnswerNpc(1021)
		self.finalExamNpcObj = npcObj

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		if npcIdx == 1021:
			return FinalExamNpc(self)
		return customActivity.newNpc(self, npcIdx, name, shape, who)

	def deleteFinalExamNpc(self):
		'''删除NPC
		'''
		if not self.finalExamNpcObj:
			return
		self.removeNpcByTypeFlag("finalExam")
		self.finalExamNpcObj = None

	def getFinalExamNpc(self):
		return self.finalExamNpcObj

	def getQuestionConfig(self, iNo, sKey='', default=None):
		if iNo not in QuestionFinalData.gdData:
			raise Exception,"殿试答题题库{}编号问题不存在".format(iNo)
		if not sKey:
			return QuestionFinalData.gdData[iNo]
		return QuestionFinalData.gdData[iNo].get(sKey, default)

	def errAddTime(self):
		'''回答错误增加秒数
		'''
		return self.getConfigInfo(3002)

	def randQuestion(self, who):
		'''抽取20题
		'''
		lAllQuestion = QuestionFinalData.gdData.keys()
		iLen = len(lAllQuestion)
		count = self.maxAnswerCnt()
		if iLen < count:
			raise Exception,"没有可用的答题题库数据"

		lDayQuestion = []
		for i in xrange(count):
			iProblemNo = lAllQuestion[rand(len(lAllQuestion))]
			lDayQuestion.append(iProblemNo)
			lAllQuestion.remove(iProblemNo)
		who.week.set("finalExamQues", lDayQuestion)	#随机问题
		who.week.set("finalExamCnt", 0)

	def startExam(self, who):
		'''开始答题
		'''
		if not self.isInAnswerTime():
			message.tips(who, self.getText(2343))
			return
		if not self.hasQualifications(who.id):
			return

		if not who.week.fetch("finalExamQues", None):
			self.randQuestion(who)
			message.tips(who, self.getText(2338))
			who.week.set("finalExamST", getSecond())	#开始时间
		#发问题给客户端
		answer.service.finalExamQuestion(who)
		self.setStartAnswer(who)	#为了不能被队伍匹配、邀请

	def answerQuestion(self, who, sResult):
		'''回答
		'''
		if self.isAnswerEnd():
			message.tips(who, self.getText(2343))
			return
		if not self.hasQualifications(who.id):
			return
		#正在回答第几题
		answerCnt = who.week.fetch("finalExamCnt", 0)
		if answerCnt >= self.maxAnswerCnt():
			return

		lFinalExamQues = who.week.fetch("finalExamQues", [])
		if not lFinalExamQues or answerCnt >= len(lFinalExamQues):
			raise Exception,"答题-殿试：{}没有生成题目就答题 {}|{}".format(who.id, answerCnt, lFinalExamQues)
			# return

		iQuestionNo = lFinalExamQues[answerCnt]
		if self.isRightAnswer(iQuestionNo, sResult):
			message.tips(who, self.getText(2339))
			# who.week.add("finalExamRight", 1)#回答题目正确数量,没什么用
			who.week.add("finalExmaRightN", 1)#连续正确题数
			self.doScript(who, None, "R{}".format(4001))
		else:
			message.tips(who, self.getText(2340))
			who.week.add("finalExamErr", 1)#回答题目正确数量
			who.week.set("finalExmaRightN", 0)#连续正确题数
			self.doScript(who, None, "R{}".format(4006))

		answerCnt = who.week.add("finalExamCnt", 1)	#回答题目数量
		who.week.set("finalExamET", getSecond())	#结束时间
		#更新排行榜
		self.updateFinalExamRank(who)

		#加活跃
		perPoint = activity.center.getPerActPoint(18)
		who.addActPoint(perPoint)

		if answerCnt >= self.maxAnswerCnt():
			iUseTime = self.getFinalExamUseTime(who)
			message.tips(who, "你已回答完所有的金章之试题目，耗时#C02{}#n，请关注#C0222:30#n的结果公布".format(formatTime(iUseTime)))
			who.endPoint.rpcFinalExamComplete(iUseTime)
			self.setEndAnswer(who)
			return
		if self.isAnswerEndFiveMin():
			iUseTime = self.getFinalExamUseTime(who)
			message.tips(who, "你未在#C0222:00#n之前完成所有的金章之试答题，耗时#C02{}#n，请关注#C0222:30#n的结果公布".format(formatTime(iUseTime)))
			self.setEndAnswer(who)
			return

		self.startExam(who)

	def getFinalExamUseTime(self, who):
		'''当前考试耗时
		'''
		iErrCnt = who.week.fetch("finalExamErr", 0)
		iTime = getSecond() - who.week.fetch("finalExamST", 70*60) + iErrCnt*self.errAddTime()
		return iTime

	def getValueByVarName(self, varName, who):
		if varName == "N":#连续答对的题数
			return who.week.fetch("finalExmaRightN", 0)
		elif varName == "X":#当前题目数
			return who.week.fetch("finalExamCnt", 0) + 1
		return customActivity.getValueByVarName(self, varName, who)

	def resetRank(self):
		'''周六00:00清空排行榜
		'''
		self.answerLog("finalExam", "resetRank")
		rankObj = rank.getRankObjByName("rank_finalExam")
		rankObj.clearRank()

	def updateFinalExamRank(self, who):
		'''更新排行榜
		'''
		if not self.isInAnswerTime():
			return
		iMaxAnswerCnt = self.maxAnswerCnt()
		#完成情况 1:已答完 2:未答完, 3:未参加
		cnt = who.week.fetch("finalExamCnt", 0)	#回答题目数量
		com = 3
		if cnt >= iMaxAnswerCnt:
			com = 1
		elif cnt > 0:
			com = 2
		comTime = 0	#完成时间
		iErrCnt = who.week.fetch("finalExamErr", 0)
		if com == 1:
			comTime = who.week.fetch("finalExamET", 0) - who.week.fetch("finalExamST", 0) + iErrCnt*self.errAddTime()
		elif com == 2:
			comTime = who.week.fetch("finalExamET", 0) - who.week.fetch("finalExamST", 0) + iErrCnt*self.errAddTime()
			comTime += 30 * max(0, iMaxAnswerCnt - who.week.fetch("finalExamCnt", 0))
		else:
			comTime = 70*60

		#初试耗时
		firstExamObj = answer.getAnswerFirstExamObj()
		firstExamTime = firstExamObj.getFirstAnswerTime(who, iMaxAnswerCnt)

		rank.updateFinalExamRank(who, com, comTime, firstExamTime)

	def setEndTimer(self):
		date = getDatePart()
		wday = date["wday"]
		if wday != 6:
			return
		curHour = date["hour"]
		if curHour != 22:
			return
		curMinute = date["minute"]
		if curMinute >=30:
			return
			
		lEndTime = []
		lEndTime.append(date["year"])
		lEndTime.append(date["month"])
		lEndTime.append(date["day"])
		lEndTime.append(22)
		lEndTime.append(30)
		lEndTime.append(0)

		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		self.answerLog("finalExam", "setEndTimer|{}".format(iLeftTime))
		self.timerMgr.run(self.publicResult, iLeftTime, 0, "publicResult")

	def publicResult(self):
		'''公布结果
		'''
		self.stopTimer("publicResult")
		self.answerLog("finalExam", "publicResult start")
		#排行榜手动排序一次
		rankObj = rank.getRankObjByName("rank_finalExam")
		rankObj.clearFinalExamRank()
		rankObj.timerUpdateRanking()

		lFinalResult = rankObj.lRanking
		self.week.set("finalResult", lFinalResult)

		if not lFinalResult:
			self.answerLog("finalExam", "publicResult:not lFinalResult")
			# return

		#系统传闻+滚屏公告
		if lFinalResult:
			# dTitle = {1:"天问魁首{}、", 2:"天问次座{}、", 3:"天问敬座{}！"}
			# lTempStr = ["本次金章之试的前三名是："]
			dTempStr = {
				1:'本次金章之试的第一名是：天问魁首#C01{}#n',
				2:'本次金章之试的前两名是：天问魁首#C01{}#n、天问次座#C01{}#n',
				3:'本次金章之试的前三名是：天问魁首#C01{}#n、天问次座#C01{}#n、天问敬座#C01{}#n',
			}
			lTitleRole = lFinalResult[:3]
			lName = []
			for index,iRoleId in enumerate(lTitleRole):
				#可能不在线,从排行榜拿名字
				name = rankObj.getRoleName(iRoleId)
				# lTempStr.append(dTitle[index+1].format(name))
				lName.append(name)
			content = dTempStr.get(len(lTitleRole)).format(*lName)#"".join(lTempStr)
			message.sysMessage(content)
			message.sysRoll(content)

		#发邮件
		# dTitle = {1:"天问魁首", 2:"天问次座", 3:"天问敬座"}
		sTitle = "金章之试奖励"
		content = "恭喜你在本周金章之试中取得了第{}名的成绩，你获得了称号{}和丰厚的排名奖励！"
		iTitleEndTime = self.getTitleEndTime()	#称号结束时间
		for index,iRoleId in enumerate(lFinalResult):
			iRank = index+1
			sTitleName = getFinalExamTitleName(iRank)#dTitle.get(iRank, "天问末座")
			sTempContent = content.format(iRank, sTitleName)
			mail.sendSysMail(iRoleId, sTitle, sTempContent)

			who = getRole(iRoleId)
			#奖励 称谓奖励
			iRewardIdx = gdFinalExamRewardIdx.get(iRank, giOtherRewardIdx)	#默认是4005奖励
			if who:
				self.doScript(who, None, "R{}".format(iRewardIdx))
				title.newTitle(who, gdFinalExamTitleNo.get(iRank, giFinalExamOtherTitleNo), et=iTitleEndTime)
			else:#离线发奖励
				offlineHandler.addHandler(iRoleId, "finalExamReward", iRank=iRank,iRewardIdx=iRewardIdx, iTitleEndTime=iTitleEndTime)

		#投注献花统计
		if lFinalResult:
			betFlowerObj = answer.getBetFlowerObj()
			betFlowerObj.statisticsResult(lFinalResult[0])

	def getTitleEndTime(self):
		'''本次称谓结束时间,到下一个周六22:00的秒数
		'''
		date = getDatePart()
		wday = date["wday"]
		day = date["day"]
		if wday >= 6: #现在是星期六或日
			day += (6+(7-wday))
		else:
			day += (6-wday)

		lEndTime = []
		lEndTime.append(date["year"])
		lEndTime.append(date["month"])
		lEndTime.append(day)
		lEndTime.append(22)
		lEndTime.append(0)
		lEndTime.append(0)

		iEndTime = getSecond(*lEndTime)
		return iEndTime

	def offlineReward(self, who, **kwargs):
		'''离线玩家上线发奖励
		'''
		iRewardIdx = kwargs.get("iRewardIdx", 0)
		if iRewardIdx:
			self.doScript(who, None, "R{}".format(iRewardIdx))

		iTitleEndTime = kwargs.get("iTitleEndTime", 0)
		iRank = kwargs.get("iRank", 0)
		if iTitleEndTime > getSecond() and iRank:
			title.newTitle(who, gdFinalExamTitleNo.get(iRank, giFinalExamOtherTitleNo), et=iTitleEndTime)

class FinalExamNpc(customNpc):
	'''金章之试NPC
	'''
	# def __init__(self, gameObj):
	# 	npc.object.NpcBase.__init__(self)
	# 	self.game = weakref.proxy(gameObj)

	# def remove(self):
	# 	sceneObj = scene.getScene(self.sceneId)
	# 	if sceneObj:
	# 		sceneObj.removeEntity(self)

	def checkCanExam(self, who):
		if who.level < 20:
			return False#'少侠等级太低，请升到#C04 20级#n后再来'
		return True

	def getFinalExamChat(self, who):
		date = getDatePart()
		wday = date["wday"]
		curHour = date["hour"]
		chat = ''
		#除周六20:00-24:00外所有时间显示
		if wday == 6:
			if curHour >= 20 and curHour < 21:
				chat = '金章之试名单已出炉，请留意邮箱并关注#C04 21:00 #n开始的金章之试'
			elif curHour >= 21 and curHour < 22:
				answerCnt = who.week.fetch("finalExamCnt", 0)
				if self.game.hasQualifications(who.id):
					if answerCnt >= self.game.maxAnswerCnt():
						chat = '你已完成了本周的金章之试，请关注#C04 22:30 #n的金章之试结果公布'
					else:
						chat = '金章之试已经开始，是否开始答题？'
				else:
					chat = '你未获得本周的金章之试参与资格，请下周继续努力！'
			elif curHour >= 22:
				chat = '金章之试已结束，请关注#C04 22:30 #n的金章之试结果公布'
		if not chat:
			chat = '金章之试于 #C04每周六21点#n 开始，参与天问初试可获得金章之试的参与资格'

		return chat

	def doLook(self, who):
		txtList= []
		selList = []
		txtList.append(self.getFinalExamChat(who))

		date = getDatePart()
		wday = date["wday"]
		curHour = date["hour"]
		curMinute = date["minute"]

		bShowRank = True
		if wday == 6:#周六12:00-22:30以外的所有时间显示
			if curHour >= 12 and (curHour <= 22 and curMinute < 30):
				bShowRank = False
		else:
			bShowRank = True

		bCanExam = self.checkCanExam(who)

		if gbNotLimitTime or (bShowRank and bCanExam):
			txtList.append('Q金章之试排名')
			selList.append(101)
		if wday == 6:
			answerCnt = who.week.fetch("finalExamCnt", 0)
			if gbNotLimitTime or (bCanExam and \
				(curHour >= 21 and curHour < 22 and self.game.hasQualifications(who.id) and answerCnt < self.game.maxAnswerCnt())
				):
				txtList.append('Q开始答题')
				selList.append(102)
		
		content = "\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return

		sel = selList[selectNo-1]
		if sel == 101:	#金章之试排名
			openUIPanel.openRankUi(who, 10901)
		elif sel == 102:#开始答题
			if who.getTeamObj():
				message.tips(who, self.game.getText(2321, who.id))
				return
			self.game.startExam(who)


#=======================================
def finalExamOfflineReward(who, **kwargs):
	'''离线uqdd
	'''
	finalExamObj = answer.getAnswerFinalExamObj()
	finalExamObj.offlineReward(who, **kwargs)

def getFinalExamTitleName(iRank):
	'''称号名字
	'''
	iTitleId = gdFinalExamTitleNo.get(iRank, giFinalExamOtherTitleNo)
	titleObj = title.getTitle(iTitleId)
	return titleObj.name


from common import *
from answer.defines import *
import timer
import answer
import answer.service
import log
import message
import QuestionFinalData
import misc
import openUIPanel
import scene
import weakref
import rank
import rank.service
import cycleData
import resume
import mail
import npc
import title
import activity.center
import offlineHandler