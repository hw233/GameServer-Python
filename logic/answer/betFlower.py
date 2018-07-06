# -*- coding: utf-8 -*-
from answer.object import cAnswerBase as customActivity

class Activity(customActivity):
	'''答题-投注献花
	'''
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.week=cycleData.cCycWeek(2, self.markDirty)
		self.reset()

	def reset(self):
		'''重置
		'''
		pass

	def init(self):
		pass

	def load(self,dData):#override
		customActivity.load(self, dData)
		self.week.load(dData.pop('w',{}))

	def save(self):#override
		dData = customActivity.save(self)
		dHour=self.week.save()
		if dHour:
			dData['w']=dHour
		return dData

	def isInBetTime(self):
		'''周六20:00-21:00
		'''
		if gbNotLimitTime:
			return True

		date = getDatePart()
		wday = date["wday"]

		if wday == 6:
			curHour = date["hour"]
			if curHour >= 20 and curHour < 21:
				return True
		return False

	def getTargetName(self, iTargetRoleId):
		'''献花对象名字
		'''
		firstExamObj = answer.getAnswerFirstExamObj()
		rankObj = firstExamObj.getFinalRank()
		sTargetName = rankObj.getRoleName(iTargetRoleId)
		return sTargetName

	def addBetFlower(self, who, iTargetRoleId, iBetCnt):
		'''献花记录
		'''
		dBetFlower = self.week.fetch("betFlower", {})
		if iTargetRoleId not in dBetFlower:
			dBetFlower[iTargetRoleId] = {}
		if who.id not in dBetFlower[iTargetRoleId]:
			dBetFlower[iTargetRoleId][who.id] = 0
		dBetFlower[iTargetRoleId][who.id] += iBetCnt
		self.week.set("betFlower", dBetFlower)

		self.answerLog("betFlower", "addBetFlower|{}|{}|{}|{}".format(who.id, iTargetRoleId, iBetCnt, dBetFlower[iTargetRoleId][who.id]))

	def getTotalBetFlower(self, pid):
		'''总被献花数
		'''
		dBetFlower = self.week.fetch("betFlower", {})
		return sum(dBetFlower.get(pid, {}).values())

	def canBetFlower(self, who, iTargetRoleId, iBetCnt):
		'''判断是否可以献花
		'''
		if not self.isInBetTime():
			message.tips(who, self.getText(2348))
			return False
		#是否在榜上
		finalExamObj = answer.getAnswerFinalExamObj()
		if not finalExamObj.hasQualifications(iTargetRoleId):
			#没上榜
			return False
		#献花记录
		dBetFlowerRecord = who.day.fetch("betFRecord", {})
		if dBetFlowerRecord.get(iTargetRoleId, 0) >= giMaxBetFlower:
			message.tips(who, "你对#C01{}#n献花已达#C04{}朵#n，无法继续献花".format(self.getTargetName(iTargetRoleId),giMaxBetFlower))
			return False
		return True
	
	def betFlower(self, who, iTargetRoleId, iBetCnt):
		'''献花
		'''
		#献花记录
		dBetFlowerRecord = who.day.fetch("betFRecord", {})
		iLeftCnt = giMaxBetFlower - dBetFlowerRecord.get(iTargetRoleId, 0)	#最多可献花数量
		bFlag = True
		if iBetCnt > iLeftCnt:	#超过可献花数量
			iBetCnt = iLeftCnt
			bFlag = False
		if not self.canBetFlower(who, iTargetRoleId, iBetCnt):
			return

		#扣物品
		who.propsCtn.subPropsByNo(giFlowerPropsNo, iBetCnt, "献花投注")
		#记录对谁献花
		dBetFlowerRecord[iTargetRoleId] = dBetFlowerRecord.get(iTargetRoleId, 0) + iBetCnt
		who.day.set("betFRecord", dBetFlowerRecord)
		#增加献花记录
		self.addBetFlower(who, iTargetRoleId, iBetCnt)

		sTargetName = self.getTargetName(iTargetRoleId)
		if bFlag:
			message.tips(who, "你成功的对#C01{}#n献出#C02{}#n朵鲜花".format(sTargetName, iBetCnt))
		else:
			message.tips(who, "对同一名玩家献花累计不可超过#C04{}朵#n，你成功的对#C01{}#n献出了#C02{}朵#n献花".format(giMaxBetFlower, sTargetName, iBetCnt))
		
	def statisticsResult(self, iFirstRoleId):
		'''22:30时，统计兑换点 = 未投中的鲜花数量/投中的鲜花数量，之后奖励投中玩家积分 = 投注的鲜花数量 * 兑换点 * $number / 100
		'''
		self.answerLog("betFlower", "statisticsResult|{}".format(iFirstRoleId))
		self.week.set("firstRoleId", iFirstRoleId)		#第一名

		dBetFlower = self.week.fetch("betFlower", {})
		iOtherCnt = 0 		#未投中的鲜花数量
		iLotteryCnt = 0 	#投中的鲜花数量
		for pid,dInfo in dBetFlower.iteritems():
			if pid == iFirstRoleId:
				iLotteryCnt = sum(dInfo.values())
			else:
				iOtherCnt += sum(dInfo.values())

		if not iLotteryCnt:#没人投中
			self.answerLog("betFlower", "statisticsResult not iLotteryCnt|{}|{}".format(iLotteryCnt, iOtherCnt))
			return

		percent = (iOtherCnt*1.0)/iLotteryCnt
		#奖励投中的玩家积分
		oProps = props.getCacheProps(giFlowerPropsNo)
		if not oProps:
			raise Exception,"献花没有天问鲜花数据"

		iPrice = oProps.getConfig("出售价格")
		dLotteryInfo = dBetFlower.get(iFirstRoleId, {})	#投中玩家

		oResume = resume.getResume(iFirstRoleId)
		sTitle1 = "天问献花奖励"
		sTitle2 = "天问献花结果"
		sContent2 = "你在本周天问献花声援的玩家没有获得金章之试的第一名，请不要灰心再接再厉！"
		for pid,dInfo in dBetFlower.iteritems():
			if pid == iFirstRoleId:	#投中玩家
				for _pid,iBetCnt in dInfo.iteritems():
					iPoint = int(percent*(iPrice/100)*iBetCnt)
					propsObjList = []
					propsObj = props.new(giFlowerPointPropsNo)
					if propsObj.isVirtual():
						propsObj.setValue(iPoint)
					else:
						propsObj.setStack(iPoint)
					propsObjList.append(propsObj)
					sContent = "你在本周天问献花声援的{}获得了金章之试的第一名，因此你获得了{}点献花积分！".format(oResume.fetch("name"), iPoint)
					mail.sendSysMail(_pid, sTitle1, sContent, propsObjList)
					self.answerLog("betFlower", "statisticsResult reward|{}|{}|{}".format(_pid, iBetCnt, iPoint))
			else:
				for _pid,iBetCnt in dInfo.iteritems():
					mail.sendSysMail(_pid, sTitle2, sContent2)

		# for pid,iBetCnt in dLotteryInfo.iteritems():
		# 	iPoint = int(percent*(iPrice/100)*iBetCnt)
		# 	mail.sendSysMail(who.id, title, content, propsObjList
			# who = getRole(pid)
			# if who:
			# 	launch.launchBySpecify(who, giFlowerPointPropsNo, iPoint, False, "统计兑换点")
			# else:
			# 	# 离线给献花积分
			# 	offlineHandler.addHandler(pid, "finalExamReward", point=iPoint)

	def getBetFlowerInfo(self, who, iRankIdx=0, iTargetRoleId=0):
		'''献花信息
		'''
		firstExamObj = answer.getAnswerFirstExamObj()
		rankObj = firstExamObj.getFinalRank()
		if iRankIdx > len(rankObj.lRanking):
			return None
		if not iTargetRoleId:
			iTargetRoleId = rankObj.lRanking[iRankIdx-1]
		finalExamObj = answer.getAnswerFinalExamObj()
		if not finalExamObj.hasQualifications(iTargetRoleId):
			#没上榜
			return None

		msg = {}
		msg["iTargetRoleId"] = iTargetRoleId
		msg["sName"] = rankObj.getRoleName(iTargetRoleId)			#名字
		msg["iLevel"] = rankObj.getRoleLv(iTargetRoleId)			#等级
		msg["iSchool"] = rankObj.getRoleSchool(iTargetRoleId)		#职业
		msg["iGender"] = rankObj.getRoleGender(iTargetRoleId)		#性别
		msg["iTotalBetCnt"] = self.getTotalBetFlower(iTargetRoleId)	#总被献花数量
		dBetFlowerRecord = who.day.fetch("betFRecord", {})
		msg["iBetCnt"] = dBetFlowerRecord.get(iTargetRoleId, 0)		#已献花数量
		return msg


def rpcBetFlower(who, reqMsg):
	'''献花
	'''
	iTargetRoleId = reqMsg.iTargetRoleId
	iBetCnt = reqMsg.iBetCnt
	if iBetCnt > sum(who.propsCtn.getPropsAmountByNos(giFlowerPropsNo)):
		#献花时拥有献花数小于献花数，弹出双选框4001
		content = '鲜花数量不足，是否前往商店购买？\nQ否\nQ是'
		message.confirmBoxNew(who, responseOpenShop, content)
		return

	betFlowerObj = answer.getBetFlowerObj()
	betFlowerObj.betFlower(who, iTargetRoleId, iBetCnt)
	msg = betFlowerObj.getBetFlowerInfo(who, 0, iTargetRoleId)
	if not msg:
		return
		# raise Exception,"非法请求"
	who.endPoint.rpcBetFlowerInfoChange(**msg)

def responseOpenShop(who, yes):
	if not yes:
		return
	#弹出商店
	shop.openShop(who, giFlowerShopNpcNo)

def rpcBetFlowerInfoReq(who, reqMsg):
	'''献花操作信息
	'''
	iRankIdx = reqMsg.iValue
	betFlowerObj = answer.getBetFlowerObj()
	msg = betFlowerObj.getBetFlowerInfo(who, iRankIdx)
	if not msg:
		return
		# raise Exception,"非法请求"
	who.endPoint.rpcBetFlowerInfoRes(**msg)


def rpcBetFlowerMainReq(who, reqMsg):
	'''请求献花界面
	'''
	iPage = reqMsg.iValue if reqMsg else 1
	#入围名单
	finalExamObj = answer.getAnswerFinalExamObj()	
	lFinalExamRole = finalExamObj.getFinalExamList()
	#入围时排行榜
	firstExamObj = answer.getAnswerFirstExamObj()
	rankObj = firstExamObj.getFinalRank()

	iLen = len(lFinalExamRole)
	iStart = (iPage-1)*20
	iEnd = min(iLen, iPage*20)

	msg = answer_pb2.betFlowerMain()
	msg.iMaxPage = iLen/20+1 if iLen%20 else iLen/20
	lTempMsg = []
	for index,iRoleId in enumerate(lFinalExamRole[iStart:iEnd]):
		betRoleInfoMsg = answer_pb2.betRoleInfo()
		betRoleInfoMsg.iRank = (iPage-1)*20+index+1
		betRoleInfoMsg.sName = rankObj.getRoleName(iRoleId)
		betRoleInfoMsg.sGuildName = rankObj.getGuildName(iRoleId)
		betRoleInfoMsg.iTime = rankObj.getValue(iRoleId)

		lTempMsg.append(betRoleInfoMsg)
	msg.lBetRoleInfo.extend(lTempMsg)
	who.endPoint.rpcBetFlowerMain(msg)


from common import *
from answer.defines import *
import timer
import answer
import answer.service
import log
import message
import openUIPanel
import rank
import cycleData
import mail
import answer_pb2
import launch
import offlineHandler
import shop
import props
import resume