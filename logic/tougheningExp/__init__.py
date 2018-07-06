# -*- coding: utf-8 -*-
'''历练经验 experience and toughening
'''

if "gbOnce" not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV:
		gdTougheningExpObj = {}

def init():
	role.geOffLine += roleOffLine
	initTougheningExpObj()
	initTransformRange()

def initTougheningExpObj():
	global gdTougheningExpObj
	gdTougheningExpObj = {}
	for actId,_ in tougheningExpData.gdData.iteritems():
		obj = tougheningExp.object.TougheningExp(actId)
		gdTougheningExpObj[actId] = obj

def getTougheningExpObj(actId):
	if actId not in gdTougheningExpObj:
		raise Exception,"历练经验对象不存在:{}".format(actId)
	return gdTougheningExpObj[actId]

def roleOffLine(who):
	'''记录对应的任务进度或活动进度
	'''
	dActProgress = getAllActProgess(who)
	who.set("actProgress", dActProgress)

def getAllActProgess(who, iWhichCyc=0):
	'''所有活动的进度
	'''
	centerObj = activity.center.getActivityCenter()
	dActProgress = {}
	for actId,obj in gdTougheningExpObj.iteritems(): 
		actObj = centerObj.actList.get(actId, None)
		if not actObj:
			continue
		iCnt = actObj.getCnt(who, iWhichCyc)
		if iCnt:
			dActProgress[actId] = iCnt

		if obj.name == "天问初试":
			iCnt = who.week.fetch("firstExmaRightN", 0)
			if iCnt:
				dActProgress["firstExmaRightN"] = iCnt
	return dActProgress

def beforeLogin(who, bReLogin):
	'''	为了拿上一次登录的dayNo，要在who.checkDayNo()之前调用
		根据玩家下线时记录的活动进度，计算成对应的历练经验
		计算玩家从离线到上线中间经历过的天数，并根据“历练经验”导表计算出每天所能获得的历练经验
	'''
	rewardTougheningExp(who)

def onNewDay(who):
	'''刷天补偿历练经验
	'''
	rewardTougheningExp(who, -1)

def rewardTougheningExp(who, iWhichCyc=0):
	'''登录和刷天奖励历练经验 iWhichCyc=-1是刷天,=0是登录
	'''
	if who.day.fetch("calcToughening", 0):
		return
	who.day.set("calcToughening", 1)
	if who.fetch("newbie"):
		return
	lastDayNo = who.fetch("dayNo")	#上次登录的天变量
	if iWhichCyc == -1:			#刷天时lastDayNo为今天的天变量
		lastDayNo -= 1
	dayNoNow = getDayNo()		#今天的变量

	lLog = ["id={}".format(who.id), "lastDayNo:{}".format(lastDayNo), "dayNoNow:{}".format(dayNoNow)]
	iRewardExp = 0
	iCurExp = who.getTougheningExp()		#当前的历练经验

	iOfflineDay = max(0, dayNoNow-lastDayNo-1)	#中间没登录天数，如上次登录是10，现在是15，则为4天没登录过
	if iOfflineDay:
		#每天错过的经验不一样
		for iDayNo in xrange(lastDayNo+1, dayNoNow):
			for actId,obj in gdTougheningExpObj.iteritems(): 
				iRewardExp += obj.calculateExp(who, iDayNo, 0)
				if iRewardExp + iCurExp >= MAX_GHOUGHENING_EXP:	#超过上限不再计算
					break
			if iRewardExp + iCurExp >= MAX_GHOUGHENING_EXP:	#超过上限不再计算
				break

		lLog.append("iOfflineDay={} iRewardExp={}".format(iOfflineDay, iRewardExp))
	else:
		lLog.append("iOfflineDay={}".format(iOfflineDay))

	if iRewardExp + iCurExp >= MAX_GHOUGHENING_EXP:	#超过上限不再计算
		lLog.append("MAX_GHOUGHENING_EXP iCurExp={} iRewardExp={}".format(iCurExp, iRewardExp))
		iRewardExp = MAX_GHOUGHENING_EXP - iCurExp
	else:	#计算上次登录当天的历练经验
		if iWhichCyc == -1:
			dActProgress = getAllActProgess(who, iWhichCyc)	#拿昨天的
		else:
			dActProgress = who.fetch("actProgress", {})		#拿最后下线记录的进度
		lLog.append("dActProgress={}".format(dActProgress))
		for actId,obj in gdTougheningExpObj.iteritems():
			iAddExp = obj.calculateExp(who, lastDayNo, dActProgress.get(actId, 0))
			iRewardExp += iAddExp
			lLog.append("actId={} iAddExp={}".format(actId, iAddExp))
			if iRewardExp + iCurExp >= MAX_GHOUGHENING_EXP:	#超过上限不再计算
				iRewardExp = MAX_GHOUGHENING_EXP - iCurExp
				break
	
	lLog.append("iRewardExp={}".format(iRewardExp))
	if iRewardExp:
		if iWhichCyc == -1:
			who.addTougheningExp(iRewardExp, "刷天补偿历练经验")
			content = "昨天错过的日常活动已转化为#C02{}#n点#C02历练经验#n，完成日常活动时，历练经验将会转化为人物经验".format(iRewardExp)
		else:
			who.addTougheningExp(iRewardExp, "上线补偿历练经验", bRefresh=False)
			content = "之前错过的日常活动已转化为#C02{}#n点#C02历练经验#n，完成日常活动时，历练经验将会转化为人物经验".format(iRewardExp)
			
		message.message(who, content)
		message.tips(who, content)

		#发送邮件
		content = '错过的日常活动已转化为#C07{}#n点#C07历练经验#n，完成日常活动时，历练经验将会转化为人物经验'.format(iRewardExp)
		friend.sendSysMsg(who.id, content)
		# mail.sendSysMail(who.id, '历练经验', content, validTime=168*3600)

	if config.IS_INNER_SERVER:
		sLog = "|".join(lLog)
		writeLog("tougheningExp", sLog)
		# print sLog
		# message.message(who, "\n".join(lLog))

def tougheningExpTransform(who, iVal, sReason):
	'''玩家获得任何人物经验时，程序判定历练经验是否 = 0，如果 != 0，则
		理论额外人物经验 = 本应获得的人物经验 * 转化系数
		实际额外人物经验 = min(理论额外人物经验,历练经验)
		历练经验 = 历练经验 - 实际额外人物经验
		玩家实际获得的人物经验 = 本应获得的人物经验 + 实际额外人物经验
	'''
	if not isInTransformRange(sReason):
		return 0
	iTougheningExp = who.getTougheningExp()
	if not iTougheningExp:
		return 0
	iTheoryExp = int(iVal*0.6)	#理论额外人物经验
	iActualExp = min(iTheoryExp, iTougheningExp)#理论额外人物经验
	who.addTougheningExp(-iActualExp, "历练经验转化")
	return iActualExp


from common import *
from tougheningExp.defines import *
import tougheningExp.object
import timerEvent
import role
import tougheningExpData
import activity.center
import message
# import mail
import friend
import config


def testInstruction(ep, who, cmdIdx, *args):
	cmdIdx = int(cmdIdx)

	if cmdIdx == 100:
		txtList = []
		txtList.append("101-重置今日是否获得历练经验")
		txtList.append("102-重置历练经验为0")
		txtList.append("103-查看历练经验")
		txtList.append("104-增加历练经验")
		message.dialog(who, "\n".join(txtList))

	if cmdIdx == 101:#重置今日是否获得历练经验
		who.day.set("calcToughening", 0)

	elif cmdIdx == 102:#重置历练经验为0
		who.addTougheningExp(-who.getTougheningExp(), "指令")

	elif cmdIdx == 103:#查看历练经验
		message.tips(who, "你的#C02历练经验#n为#C02{}#n点".format(who.getTougheningExp()))

	elif cmdIdx == 104:#增加历练经验
		who.addTougheningExp(int(args[0]), "指令")

	elif cmdIdx == 200:
		beforeLogin(who, False)

	elif cmdIdx == 201:	#
		initTougheningExpObj()

	elif cmdIdx == 202:	#重置初始化转化经验范围
		initTransformRange()

	elif cmdIdx == 203:
		roleOffLine(who)
		
