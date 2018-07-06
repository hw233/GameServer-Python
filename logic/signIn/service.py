# -*- coding: utf-8 -*-
import endPoint
import signIn_pb2

class cService(signIn_pb2.terminal2main):

	@endPoint.result
	def rpcSignInOpen(self, ep, who, reqMsg): return rpcSignInOpen(who, reqMsg)
	
	@endPoint.result
	def rpcSignIn(self, ep, who, reqMsg): return rpcSignIn(who, reqMsg)

def rpcSignInOpen(who, reqMsg):
	'''请求打开签到界面
	'''
	if reqMsg.signType == signIn.DAY_SIGNIN:
		rpcSignInMsg(who)
	elif reqMsg.signType == signIn.GUILD_SIGNIN:
		guildSignInOpen(who)

def rpcSignIn(who, reqMsg):
	'''签到
	'''
	if reqMsg.signType == signIn.DAY_SIGNIN:
		daySignIn(who)
	elif reqMsg.signType == signIn.GUILD_SIGNIN:
		guildSignIn(who)

def rpcSignInMsg(who):
	msg = {}
	msg["signType"] = signIn.DAY_SIGNIN
	msg["signCount"] = who.month.fetch("signCount", 0)
	msg["signIn"] = who.day.fetch("signIn", 0)
	msg["signAgain"] = who.day.fetch("signAgain", 0)
	who.endPoint.rpcSignInMsg(**msg)

def daySignIn(who):
	datePart = getDatePart()
	day = datePart["day"]
	if who.month.fetch("signCount", 0) >= day:
		message.tips(who, "今天已签到")
		return

	if not who.day.fetch("signIn", 0):	#正常签到
		 who.day.set("signIn", 1)
		 message.tips(who, "签到成功")
	else:	#补签
		if who.day.fetch("signAgain", 0):
			message.tips(who, "一天只能补签一次")
			return
		else:
			if who.day.fetch("actPoint", 0) >= 80:	#补签
				who.day.set("signAgain", 1)
				message.tips(who, "补签成功")
			else:
				message.tips(who, "活跃不足")
				return
	signIn.giveSignInReward(who)
	rpcSignInMsg(who)


#============================================
#帮派签到
def rpcGuildSignInMsg(who):
	msg = {}
	msg["signType"] = signIn.GUILD_SIGNIN
	msg["signCount"] = who.week.fetch("guildSignCount", 0)
	msg["signIn"] = who.day.fetch("guildSignIn", 0)
	msg["signAgain"] = who.day.fetch("guildSignAgain", 0)
	who.endPoint.rpcSignInMsg(**msg)

def guildSignInOpen(who):
	'''请求打开帮派签到界面
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你已经被逐出本盟")
		return
	rpcGuildSignInMsg(who)

def guildSignIn(who):
	'''帮派签到
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你已经被逐出本盟")
		return

	datePart = getDatePart()
	wday = datePart["wday"]
	if who.week.fetch("guildSignCount", 0) >= wday:
		message.tips(who, "今天已签到")
		return
	if not who.day.fetch("guildSignIn", 0):	#正常签到
		 who.day.set("guildSignIn", 1)
		 message.tips(who, "签到成功")
	else:	#补签
		if who.day.fetch("guildSignAgain", 0):
			message.tips(who, "一天只能补签一次")
			return
		else:
			if who.day.fetch("actPoint", 0) >= 120:	#补签
				who.day.set("guildSignAgain", 1)
				message.tips(who, "补签成功")
			else:
				message.tips(who, "活跃不足")
				return
	signIn.giveGuildSignInReward(who)
	rpcGuildSignInMsg(who)

from common import *
import signIn
import message