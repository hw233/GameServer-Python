# -*- coding: utf-8 -*-

#每天签到
DAY_SIGNIN = 1 #每日签到
GUILD_SIGNIN = 2 #帮派签到

def isFebruaryLastDay(day):  #是否是当前月的最后一天
	'''2月份的签到最后一天为豪华签到礼包
		最后一天读取第30天的数据
	'''
	datePart = getDatePart()
	month = datePart["month"]
	if month != 2:
		return False
	year = datePart["year"]
	if (year % 4 == 0) and (year % 100 !=0) or (year % 400 == 0):
		return day == 29
	else:
		return day == 28

def getSignInReward(signCount):
	'''获取每日签到奖励数据
	'''
	if isFebruaryLastDay(signCount):
		signCount = 30
	reward = SignInData.gdData.get(signCount, {})
	if not reward:
		raise Exception,"每天签到第{}天没有奖励数据".format(signCount)
	iPropNo = reward.get("奖励编号", 0)
	iCount = reward.get("数量", 0)
	if not iPropNo or not iCount:
		raise Exception,"每天签到奖励物品编号或数量为0，{}|{}|{}".format(signCount, iPropNo, iCount)
	return {iPropNo:iCount}

def getGuildSignInReward(signCount):
	'''获取帮派签到奖励数据
	'''
	reward = GuildSignInData.gdData.get(signCount, {})
	if not reward:
		raise Exception,"帮派签到第{}天没有奖励数据".format(signCount)
	iPropNo = reward.get("道具", 0)
	iCount = reward.get("数量", 0)
	if not iPropNo or not iCount:
		raise Exception,"帮派签到奖励物品编号或数量为0，{}|{}|{}".format(signCount, iPropNo, iCount)
	return {iPropNo:iCount}

def rewardProps(who, dReward, reason="签到"):
	for iPropNo,iCount in dReward.iteritems():
		# if iPropNo == 200001:	#银币
		# 	who.rewardCash(iCount, reason)
		# elif iPropNo == 200002:	#元宝
		# 	who.addTradeCash(iCount, reason)
		# elif iPropNo == 200003:	#龙纹玉
		# 	who.addMoneyCash(iCount, reason)
		# elif iPropNo == 200004:	#门派贡献
		# 	who.addSchoolPoint(iCount, reason)
		# elif iPropNo == 200005:	#降魔积分
		# 	who.addDemonPoint(iCount, )
		# elif iPropNo == 200006:	#侠义值
		# 	who.addHelpPoint(iCount, reason)
		# elif iPropNo == 200007:	#武勋值
		# 	who.addPKPoint(iCount, reason)
		# else:#物品
		launch.launchBySpecify(who, iPropNo, iCount, False, reason)

def giveSignInReward(who):
	'''每日签到给奖励
	'''
	signCount = who.month.add("signCount", 1)
	dReward = getSignInReward(signCount)
	rewardProps(who, dReward, "每天签到")

def giveGuildSignInReward(who):
	'''帮派签到给奖励
	'''
	signCount = who.week.add("guildSignCount", 1)
	dReward = getGuildSignInReward(signCount)
	rewardProps(who, dReward, "帮派签到")

def openSingIn(who):
	signIn.service.rpcSignInMsg(who)

def onLogin(who, bReLogin):
	return	#暂时屏蔽
	if not who.day.fetch("openSingIn", 0):
		who.day.set("openSingIn", 1)
		openSingIn(who)


from common import *
import role
import SignInData
import GuildSignInData
import signIn.service
import launch
import message
#===================================================
#指令
def signInInstruction(ep, who, cmdIdx, *args):
	cmdIdx = int(cmdIdx)

	if cmdIdx == 100:
		txtList = []
		txtList.append("101-重置每日签到")
		txtList.append("102-重置每日弹出签到")
		txtList.append("103-重置每日签到")
		txtList.append("104-重置每日签到全部")

		txtList.append("201-重置帮派每日签到")
		txtList.append("202-重置帮派签到次数")
		txtList.append("203-重置帮派签到全部")

		message.dialog(who, "\n".join(txtList))

	elif cmdIdx == 101:
		who.day.set("signIn", 0)
		who.day.set("signAgain", 0)
		ep.rpcTips("重置每日签到成功")
	elif cmdIdx == 102:
		who.day.set("openSingIn", 0)
		ep.rpcTips("重置每日弹出签到成功")
	elif cmdIdx == 103:
		who.month.set("signCount", 0)
		ep.rpcTips("重置每日签到成功")
	elif cmdIdx == 104:
		who.day.set("signIn", 0)
		who.day.set("openSingIn", 0)
		who.day.set("signAgain", 0)
		who.month.set("signCount", 0)
		ep.rpcTips("重置签到全部成功")
	elif cmdIdx == 105:
		signIn.service.daySignIn(who)
	#=====================================
	#帮派
	elif cmdIdx == 201:
		who.day.set("guildSignIn", 0)
		who.day.set("guildSignAgain", 0)
		ep.rpcTips("重置帮派签到成功")
	# elif content == "gosi":
	# 	who.day.set("openSingIn", 0)
	# 	ep.rpcTips("重置每日弹出签到成功")
	elif cmdIdx == 202:
		who.month.set("guildSignCount", 0)
		ep.rpcTips("重置帮派签到成功")
	elif cmdIdx == 203:
		who.day.set("guildSignIn", 0)
		# who.day.set("openSingIn", 0)
		who.day.set("guildSignAgain", 0)
		who.week.set("guildSignCount", 0)
		ep.rpcTips("重置帮派签到全部成功")
	elif cmdIdx == 204:
		signIn.service.guildSignInOpen(who)
		signIn.service.guildSignIn(who)
#=====================================================


