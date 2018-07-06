# -*- coding: utf-8 -*-
# 交易中心服务
import endPoint
import trade_pb2
import stallService

class cService(trade_pb2.terminal2main):

	@endPoint.result
	def rpcTradeGoodsListReq(self, ep, who, reqMsg): return rpcTradeGoodsListReq(who, reqMsg)
	
	@endPoint.result
	def rpcTradeGoodsReq(self, ep, who, reqMsg): return rpcTradeGoodsReq(who, reqMsg)
	
	@endPoint.result
	def rpcTradeGoodsBuy(self, ep, who, reqMsg): return rpcTradeGoodsBuy(who, reqMsg)
	
	@endPoint.result
	def rpcTradeGoodsSell(self, ep, who, reqMsg): return rpcTradeGoodsSell(who, reqMsg)

	@endPoint.result
	def rpcStallListReq(self, ep, who, reqMsg): return stallService.rpcStallListReq(who, reqMsg)

	# @endPoint.result
	# def rpcStallPropsReq(self, ep, who, reqMsg): return stallService.rpcStallPropsReq(who, reqMsg)

	@endPoint.result
	def rpcStallBuy(self, ep, who, reqMsg): return stallService.rpcStallBuy(who, reqMsg)

	@endPoint.result
	def rpcStallSellPropsReq(self, ep, who, reqMsg): return stallService.rpcStallSellPropsReq(who, reqMsg)

	@endPoint.result
	def rpcStallSell(self, ep, who, reqMsg): return stallService.rpcStallSell(who, reqMsg)

	@endPoint.result
	def rpcStallSellItemReq(self, ep, who, reqMsg): return stallService.rpcStallSellItemReq(who, reqMsg)

	@endPoint.result
	def rpcStallOneKeyGetProps(self, ep, who, reqMsg): return stallService.rpcStallOneKeyGetProps(who, reqMsg)

	@endPoint.result
	def rpcStallOneKeyGetMoney(self, ep, who, reqMsg): return stallService.rpcStallOneKeyGetMoney(who, reqMsg)

	@endPoint.result
	def rpcStallBuyItem(self, ep, who, reqMsg): return stallService.rpcStallBuyItem(who, reqMsg)	

	@endPoint.result
	def rpcStallGetProps(self, ep, who, reqMsg): return stallService.rpcStallGetProps(who, reqMsg)

	@endPoint.result
	def rpcStallGetMoney(self, ep, who, reqMsg): return stallService.rpcStallGetMoney(who, reqMsg)	

	@endPoint.result
	def rpcStallSellAgain(self, ep, who, reqMsg): return stallService.rpcStallSellAgain(who, reqMsg)	

	@endPoint.result
	def rpcStallSearch(self, ep, who, reqMsg): return stallService.rpcStallSearch(who, reqMsg)	

def rpcTradeGoodsListReq(who, reqMsg):
	'''商品列表请求
	'''
	reqType = reqMsg.reqType
	sid = reqMsg.reqNo
	goodsList = []

	tradeCenterObj = trade.getTradeCenter(reqType)
	if not tradeCenterObj:
		return

	sendTradGoodsList(who, tradeCenterObj, sid)

def rpcTradeGoodsReq(who, reqMsg):
	'''商品请求
	'''
	reqType = reqMsg.reqType
	goodsId = reqMsg.reqNo

	tradeCenterObj = trade.getTradeCenter(reqType)
	if not tradeCenterObj:
		return

	obj = tradeCenterObj.getItem(goodsId)
	if not obj:
		return

	who.endPoint.rpcTradeGoodsInfo(packGoodsDetail(who,obj))

def rpcTradeGoodsBuy(who, reqMsg):
	'''购买商品
	'''
	reqType = reqMsg.reqType
	goodsId = reqMsg.goodsId
	count = reqMsg.count
	price = reqMsg.price

	tradeCenterObj = trade.getTradeCenter(reqType)
	if not tradeCenterObj:
		return

	goodsObj = tradeCenterObj.getItem(goodsId)
	if not goodsObj:
		return

	if not checkBuyCondition(who, goodsObj, count, price):
		return

	if reqType == 1:
		if  who.cash < price:
			if not money.checkCash(who,price):
				return
			if not checkBuyCondition(who, goodsObj, count, price):#二次检查条件
				return
		name = goodsObj.getName()
		who.costCash(price,"购买商品#C02%s×%d#n" % (name,count),None)
		message.tips(who,"花费#IS#n#C02{:,}#n，获得#C02{}×{}#n".format(price,name,count))
	elif reqType == 2:
		if who.tradeCash < price:
			if not money.checkTradeCash(who,price):
				return
			if not checkBuyCondition(who, goodsObj, count, price):#二次检查条件
				return
		name = goodsObj.getName()
		who.costTradeCash(price,"购买商品#C02%s×%d#n" % (name,count),None)
		message.tips(who,"花费#IG#n#C02{:,}#n，获得#C02{}×{}#n".format(price,name,count))

	goodsObj.wave()
	goodsObj.addBuyCount(who,count)
	launch.launchBySpecify(who,goodsObj.getPropsNo(),count,True,"购买商品#C02%s×%d#n" % (name,count),None,**goodsObj.getPropsArgs())
	who.endPoint.rpcTradeGoodsInfo(packGoodsDetail(who,goodsObj))

def rpcTradeGoodsSell(who, reqMsg):
	'''商品出售
	'''
	goodsId = reqMsg.goodsId
	count = reqMsg.count
	price = reqMsg.price
	propsId = reqMsg.propsId

	goodsObj = trade.gCashTradeCenter.getItem(goodsId)
	if not goodsObj:
		return

	stack, = who.propsCtn.getPropsAmountByNos(goodsObj.getPropsNo())
	if stack < count:
		return

	maxSell = goodsObj.maxWeekSell()
	if maxSell != -1 and goodsObj.getSellCount(who) + count > maxSell:
		return

	cost = calCost(goodsObj,count,goodsObj.getBuyPrice)
	distance = cost - price
	if distance > 2 or distance <-2: #误差2以内都算正常。到时候再调整
		message.tips(who,"商品价格已发生改变，请重新出售")
		who.endPoint.rpcTradeGoodsInfo(packGoodsDetail(who,goodsObj))
		return

	if goodsObj.isLimitDown(): #跌停
		message.tips(who,"本商品库存已满，无法继续出售")
		return

	name = goodsObj.getName()
	logReason = "出售物品#C02%s×%d#n" % (name,count)
	who.propsCtn.subtractPropsByNo(goodsObj.getPropsNo(),count,logReason,None)
	who.rewardCash(price,logReason,None)
	message.tips(who, "出售#C02{}×{}#n，获得#IS#n#C02{:,}#n".format(name,count,price))

	goodsObj.wave()
	goodsObj.addSellCount(who,count)

def openTradeCenter(who, goodsNo, taskId):
	'''打开交易中心
	'''
	sid = tradeGoodsData.gdCashGoodsToSid.get(goodsNo)
	if sid:
		tradeCenterObj = trade.gCashTradeCenter
	else:
		sid = tradeGoodsData.gdTradeCashGoodSToSid.get(goodsNo)
		tradeCenterObj = trade.gTradeCashTradeCenter
	sendTradGoodsList(who, tradeCenterObj, sid, taskId)

def sendTradGoodsList(who, tradeCenterObj, sid, taskId=0):
	'''发送商品列表
	'''
	goodsList = tradeCenterObj.getItemListBysid(sid)
	if not goodsList:
		return

	msg = {}
	msg["reqNo"] = sid
	msg["goodsList"] = packGoodsList(who,tradeCenterObj,goodsList)
	msg["taskId"] = taskId
	who.endPoint.rpcTradeGoodsList(**msg)

def checkBuyCondition(who, goodsObj, count, price):
	'''检查购买条件
	'''
	if not count:
		return False

	maxBuy = goodsObj.maxWeekBuy()
	if maxBuy != -1 and goodsObj.getBuyCount(who) + count > maxBuy:
		return False

	if (count+goodsObj.maxStack()-1)/goodsObj.maxStack() > who.propsCtn.leftCapacity():
		message.tips(who,"包裹空间不足，为防止商品丢失，请清理背包再来购买")
		return False

	cost = calCost(goodsObj,count,goodsObj.getSellPrice)
	distance = cost - price
	if distance > 2 or distance <-2: #误差2以内都算正常。到时候再调整
		message.tips(who,"商品价格已发生改变，请重新购买")
		who.endPoint.rpcTradeGoodsInfo(packGoodsDetail(who,goodsObj))
		return False

	if goodsObj.isLimitUp(): #涨停
		message.tips(who,"本商品库存已空，无法继续购买")
		return False

	return True

def calCost(goodsObj, count, priceFunc):
	'''计算消耗
	'''
	waveCount = goodsObj.getWaveCount()
	wavePrice = goodsObj.getWavePrice()
	basePrice = goodsObj.getPrice()
	needWaveCount = goodsObj.needWaveCount()

	if not needWaveCount:
		return int(priceFunc() * count)
	elif waveCount + count < needWaveCount:
		cost = priceFunc() * count
		goodsObj.newWavePrice = wavePrice + cost
		goodsObj.newWaveCount = waveCount + count
		return int(cost)

	#走到这证明基础价格购买后会发生变化，可能买的物品分几部分的价格。
	cost = 0
	while count:
		oldPriceCount = needWaveCount - waveCount
		newPriceCount = min(needWaveCount,count - oldPriceCount)
		oldPriceAll   = priceFunc() * oldPriceCount
		newBasePrice  = ((oldPriceAll+wavePrice)/needWaveCount-basePrice) * goodsObj.changeRange() + basePrice #新的基础价格
		newPriceAll   = priceFunc(newBasePrice) * newPriceCount

		waveCount = newPriceCount
		wavePrice = newPriceAll
		basePrice = newBasePrice

		cost += oldPriceAll + newPriceAll
		count -= oldPriceCount + newPriceCount

	goodsObj.newWavePrice = wavePrice
	goodsObj.newWaveCount = waveCount
	goodsObj.newPrice = basePrice

	return int(cost)

def packGoodsList(who, tradeCenterObj, goodsList):
	'''打包商品列表
	'''
	lst = []
	for goodsId in goodsList:
		obj = tradeCenterObj.getItem(goodsId)
		if not obj:
			continue
		lst.append(packGoodsFirst(obj))

	return lst

def packGoodsFirst(obj):
	'''打包商品首要信息
	'''
	msg = trade_pb2.goodsInfo()
	msg.goodsId = obj.iNo
	msg.rose  = int(obj.getRose() * 10000)
	msg.price = int(obj.getPrice()*100)
	msg.goodsType = obj.getType()

	return msg

def packGoodsDetail(who, obj):
	'''打包商品详细信息
	'''
	msg = packGoodsFirst(obj)
	msg.wavePrice = int(obj.getWavePrice()*100)
	msg.waveCount = obj.getWaveCount()
	msg.buyCount  = obj.getBuyCount(who)
	msg.sellCount = obj.getSellCount(who)
	return msg

from common import *
import tradeGoodsData
import trade
import message
import money
import launch
import props
import mail