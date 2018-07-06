#-*-coding:utf-8-*-

#货币转化率
CASH_TRADECASH = 100
CASH_MONEYCASH = 10000
TRADECASH_MONEYCASH = 100

def checkCash(who,costCash):
	'''检测银币
	'''
	if who.cash >= costCash:
		return True

	iNowStamp = getSecond()
	if iNowStamp - getattr(who,"cashBox",0) < 1 :
		return
	who.cashBox = iNowStamp

	cash = costCash - who.cash
	pid = who.id
	res = message.cashLackBox(who,cash)

	who = getRole(pid)
	if not who:
		return False

	if res == 0:
		return False

	elif res == 1:
		tradeCash = int(math.ceil(float(cash)/CASH_TRADECASH))
		if not checkTradeCash(who,tradeCash):
			return False
		who.addTradeCash(-tradeCash,"元宝兑换银币",None)
		who.addCash(tradeCash*CASH_TRADECASH,"元宝兑换银币",None)
		
	elif res == 2:
		moneyCash = int(math.ceil(float(cash)/CASH_MONEYCASH))
		if not checkMoneyCash(who,moneyCash):
			return False
		who.addMoneyCash(-moneyCash,"龙纹玉兑换银币",None)
		who.addCash(moneyCash*CASH_MONEYCASH,"龙纹玉兑换银币",None)

	return who.cash >= costCash

def checkTradeCash(who,costTradeCash):
	'''检测元宝
	'''
	if who.tradeCash >= costTradeCash:
		return True

	iNowStamp = getSecond()
	if iNowStamp - getattr(who,"tradeCashBox",0) < 1:
		return
	who.tradeCashBox = iNowStamp

	tradeCash = costTradeCash - who.tradeCash
	pid = who.id
	res = message.tradeCashLackBox(who,tradeCash)

	who = getRole(pid)
	if not who:
		return False

	if res != 1:
		return False

	moneyCash = int(math.ceil(float(tradeCash)/TRADECASH_MONEYCASH))
	if not checkMoneyCash(who,moneyCash):
		return False
	who.addMoneyCash(-moneyCash,"龙纹玉兑换元宝",None)
	who.addTradeCash(moneyCash*TRADECASH_MONEYCASH,"龙纹玉兑换元宝",None)

	return who.tradeCash >= costTradeCash

def checkMoneyCash(who,costMoneyCash):
	'''检测龙纹玉
	'''
	if who.moneyCash >= costMoneyCash:
		return True

	pid = who.id
	res = message.confirmBox(who,"您的龙纹玉不足哦，需要充值吗？\nQ以后再说\nQ去充值")

	who = getRole(pid)
	if not who:
		return False

	if res != 2:
		return False
		
	who.endPoint.rpcOpenRecharge()
	return False

def moneyCash2Cash(who, iMoneyCash, iRate=CASH_MONEYCASH):
	'''龙纹玉兑换银币
	'''
	if who.moneyCash < iMoneyCash:
		return
	who.addMoneyCash(-iMoneyCash, "龙纹玉兑换银币", None)
	who.addCash(iMoneyCash*iRate, "龙纹玉兑换银币")

def tradeCash2Cash(who, iTradeCash, iRate=CASH_TRADECASH):
	'''元宝兑换银币
	'''
	if who.tradeCash < iTradeCash:
		return
	who.addTradeCash(-iTradeCash, "元宝兑换银币", None)
	who.addCash(iTradeCash*iRate, "元宝兑换铜币")

def moneyCash2TradeCash(who, iMoneyCash, iRate=TRADECASH_MONEYCASH):
	'''龙纹玉兑换元宝
	'''
	if who.moneyCash < iMoneyCash:
		return
	who.addMoneyCash(-iMoneyCash, "龙纹玉兑换元宝", None)
	who.addTradeCash(iMoneyCash*iRate, "龙纹玉兑换元宝")


from common import *
import message
import common_pb2
import math