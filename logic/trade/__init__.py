# -*- coding: utf-8 -*-

TYPE_CASH=1
TYPE_TRADE_CASH=2

def wave(propsNo, price, count, quality=0):
	'''波动
	'''
	propsNo = transGoodsNoByQuality(propsNo,quality)
	goodsObj = gCashTradeCenter.getItem(propsNo)
	if not goodsObj:
		goodsObj = gTradeCashTradeCenter.getItem(propsNo)
		if not goodsObj:
			return
	goodsObj.waveByStall(price,count)

def openTradeCenter(who, taskObj):
	'''打开交易中心
	'''
	import propsGroupData
	for propsNo, amount in taskObj.getPropsNeeded().iteritems():
		if propsGroupData.isPropsGroup(propsNo):
			propsNo = propsGroupData.getConfig(propsNo, "列表")[0]
		hasAmount = who.propsCtn.getPropsAmountByNos(propsNo)[0]
		if hasAmount >= amount:
			continue
		quality = taskObj.fetch("propsQu")
		propsObj = props.getCacheProps(propsNo)
		if not quality and propsObj.kind in (ITEM_MEDICINE_LEVEL, ITEM_FOOD):
			quality = 10
		goodsNo = transGoodsNoByQuality(propsNo,quality)
		stallGoodsNo = gStall.hasProps(goodsNo)
		if stallGoodsNo:  #摆摊有就打开摆摊
			trade.stallService.openStall(who,stallGoodsNo,taskObj.id)
		else:
			trade.service.openTradeCenter(who,goodsNo,taskObj.id)
		return

def getNpcByPropsNo(propsNo):
	'''根据物品获取npc
	'''
	return npc.getNpcByIdx(10205)

def getGoodsPrice(propsNo,quality=0):
	'''获取商品价格
	'''
	propsNo = transGoodsNoByQuality(propsNo,quality)
	goodsObj = gCashTradeCenter.getItem(propsNo)
	if not goodsObj:
		goodsObj = gTradeCashTradeCenter.getItem(propsNo)
		if not goodsObj:
			return 0,0
	return goodsObj.getType(), int(goodsObj.getSellPrice())

def transGoodsNoByQuality(propsNo,quality):
	'''根据品质转化商品编号
	'''
	if not quality:
		return propsNo
	if propsNo in foodData.gdData:
		return propsNo + tradeGoodsData.getFoodLevel(quality)*1000000
	return propsNo + tradeGoodsData.getMedicine(quality)*1000000

def getGoodsNo(propsObj):
	'''获取商品辨识编号
	'''
	goodsNo = propsObj.no()
	if isinstance(propsObj,props.food.cProps):
		quality = propsObj.quality
		goodsNo = goodsNo + tradeGoodsData.getFoodLevel(quality)*1000000
	elif isinstance(propsObj,props.medicine.levelmedicine.cProps) and propsObj.level == 3:
		quality = propsObj.quality
		goodsNo = goodsNo + tradeGoodsData.getMedicine(quality)*1000000

	return goodsNo

def getTradeCenter(tradeType):
	if tradeType == TYPE_CASH:
		return gCashTradeCenter
	elif tradeType == TYPE_TRADE_CASH:
		return gTradeCashTradeCenter
	return None

def init():
	global gCashTradeCenter,gTradeCashTradeCenter,gStall
	gCashTradeCenter = initTradeCenter("银币交易中心","cashTradeCenter")
	gTradeCashTradeCenter = initTradeCenter("元宝交易中心","tradeCashTradeCenter")
	gStall = initStall()

	timerEvent.geNewHour += update

def initTradeCenter(sChineseName,sName):
	obj = classByName[sChineseName](sChineseName,sName)
	if not obj._loadFromDB():
		obj._insertToDB(*obj.getPriKey())

	obj.init()
	return obj

def initStall():
	obj = trade.stall.cExchange()
	if not obj._loadFromDB():
		obj._insertToDB(*obj.getPriKey())

	return obj

def onLogin(who):
	itemObj = gStall.goodsListByRoleId.get(who.id)
	if itemObj:
		iPriceAll = itemObj.getPriceAll()
	else:
		iPriceAll = 0
	who.endPoint.rpcStallSellItem(iPriceAll=iPriceAll)

def update(iYear,iMonth,iDay,iHour,iWeek):
	if iHour!=22:  #22点刷新
		return
	gCashTradeCenter.update()
	gTradeCashTradeCenter.update()


from common import *
import trade.object
import trade.stall
import timerEvent
import tradeGoodsData
import props.food
import props.medicine.levelmedicine
import npc
import trade.service
import trade.stallService
import foodData
import props
from props.defines import *


classByName = {
	"银币交易中心":trade.object.cCashTradeCenter,
	"元宝交易中心":trade.object.cTradeCashTradeCenter,
}