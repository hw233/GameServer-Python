# -*- coding: utf-8 -*-
# 摆摊服务
import trade_pb2

# def rpcStallPropsReq(who, reqMsg):
# 	'''物品购买请求
# 	'''
# 	stallId = reqMsg.iValue
# 	goodsObj = trade.gStall.getGoodsObj(stallId)
# 	if not goodsObj:
# 		message.tips(who,"该物品信息已发生变化，请重新选择物品。")
# 		sendStallList(who, goodsObj.no())
# 		return

# 	who.endPoint.rpcStallProps(packStallProps(stallId))

def rpcStallListReq(who, reqMsg):
	'''列表请求
	'''
	goodsNo = reqMsg.goodsId
	order = reqMsg.order
	page = reqMsg.page

	sendStallList(who, goodsNo, order, page)

def rpcStallBuy(who, reqMsg):
	'''购买物品
	'''
	stallId = reqMsg.stallId
	count = reqMsg.count
	goodsNo = reqMsg.goodsId

	if not checkStallBuy(who,stallId,count,goodsNo):
		return

	price = trade.gStall.getGoodsPrice(stallId)
	priceAll = price * count
	if who.tradeCash < priceAll:
		if not money.checkTradeCash(who,priceAll):
			return
		#二次检查条件
		if not checkStallBuy(who,stallId,count,goodsNo):
			return

	goodsObj = trade.gStall.getGoodsObj(stallId)
	who.costTradeCash(priceAll,"摆摊购买#C02%s×%d#n" % (goodsObj.name,count),None)
	message.tips(who,"花费#IG#n#C02{:,}#n，获得#C02{}×{}#n".format(priceAll,goodsObj.name,count))
	propsFork = props.fork(goodsObj,count)
	propsFork.setStallCD(getDayNo()+7)
	dGoods = trade.gStall.addStack(stallId,count)
	launch.launchProps(who,propsFork,"摆摊购买#C02%s×%d#n" % (goodsObj.name,count),None)
	
	goodsNo = trade.getGoodsNo(goodsObj)
	sendStallList(who, goodsNo)

	sellerId = dGoods["ownerId"]
	itemObj = trade.gStall.goodsListByRoleId.get(sellerId)
	if not itemObj:
		itemObj = trade.gStall.addStallItem(sellerId)

	tradeGooos = trade.gTradeCashTradeCenter.getItem(goodsNo)
	tradeGooos.waveByStall(price,count*2)
	priceAll = int(priceAll*(1-tradeGooos.taxRate()))
	itemObj.addPrice(dGoods['itemNo'],priceAll)

	sendTradeMail(sellerId,goodsObj.name,count,priceAll)
	sellerObj = getRole(sellerId)
	if sellerObj:
		sellerObj.endPoint.rpcStallPriceAllMod(iPriceAll=itemObj.getPriceAll())

def rpcStallSellPropsReq(who, reqMsg):
	'''出售物品请求
	'''
	propsId = reqMsg.iValue
	propsObj = who.propsCtn.getItem(propsId)
	if not propsObj:
		return

	if hasattr(propsObj,"quality") and not propsObj.quality:
		return

	goodsNo = trade.getGoodsNo(propsObj)
	goodsObj = trade.gTradeCashTradeCenter.getItem(goodsNo)
	if not goodsObj:
		message.tips(who,"该物品不能出售")
		return

	goodsList = trade.gStall.getGoodListByType(goodsNo)
	msg = {}
	msg["propsId"] = propsId
	msg["goodsId"] = goodsNo
	msg["price"] = int(goodsObj.getPrice())
	msg["stallList"] = [packStallProps(stallId) for stallId in goodsList[:5]]

	who.endPoint.rpcSellPropsInfo(**msg)

def rpcStallSell(who, reqMsg):
	'''出售物品
	'''

	costAll = 0
	for sellMsg in reqMsg.sellList:
		count = sellMsg.count
		price = sellMsg.price
		costAll += getStallPoundage(count * price)

	if not money.checkCash(who,costAll):
		return

	maxRate = 0
	maxRateNo = 0
	realCost = 0
	for sellMsg in reqMsg.sellList:
		propsId = sellMsg.propsId
		count = sellMsg.count
		price = sellMsg.price

		if not count:
			continue

		propsObj = who.propsCtn.getItem(propsId)
		if not propsObj:
			message.tips(who,"没有该物品")
			continue

		if hasattr(propsObj,"quality") and not propsObj.quality:
			message.tips(who,"#C040品质#n物品不能上架")
			continue

		if hasattr(propsObj,"dGems") and propsObj.dGems:
			message.tips(who,"镶嵌物品不能上架")
			continue
		
		if propsObj.stack() < count:
			message.tips(who,"没有足够的数量")
			continue

		if propsObj.isBind():
			message.tips(who,"物品已绑定")
			continue

		if propsObj.isRare():
			message.tips(who,"珍品不能出售")
			continue

		if propsObj.getStallCD():
			continue

		goodsNo = trade.getGoodsNo(propsObj)
		goodsObj = trade.gTradeCashTradeCenter.getItem(goodsNo)
		if not goodsObj:
			message.tips(who,"物品不能出售了")
			continue

		if trade.gStall.getGoodCountByType(goodsNo) >= goodsObj.maxStallCount():
			message.tips(who,"没有足够的摊位了")
			break

		if not trade.gStall.getFreeItem(who.id):
			break

		if price < goodsObj.minStallPrice():
			message.tips(who,"已经是最低价格")
			continue

		if price > goodsObj.maxStallPrice():
			message.tips(who,"已经是最高价格")
			continue

		realCost += getStallPoundage(count*price)
		who.propsCtn.addStack(propsObj,-count)	
		propsFork = props.fork(propsObj,count)
		trade.gStall.addGoods(who.id,propsFork,price)
		taxRate = goodsObj.taxRate()
		if taxRate > maxRate:
			maxRate = taxRate
			maxRateNo = goodsNo

	if maxRateNo:
		who.costCash(realCost,"摆摊手续费",None)
		sendStallItem(who)
		who.endPoint.rpcStallSellSuccess(maxRateNo)

def rpcStallSellItemReq(who, reqMsg):
	'''摊位信息
	'''
	sendStallItem(who)

def rpcStallOneKeyGetProps(who, reqMsg):
	'''一键取回
	'''
	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	if not itemObj:
		message.tips(who,"商品已出售")
		sendStallItem(who)
		return

	if len(itemObj.goodsList) > who.propsCtn.leftCapacity():
		message.tips(who,"背包已满，无法取出")
		return

	for itemNo in xrange(1,itemObj.count+1):
		stallId = itemObj.goodsList.get(itemNo,0)
		if not stallId:
			continue
		dGoods = trade.gStall.removeGoods(stallId,False)
		obj = props.fork(dGoods["obj"])
		launch.launchProps(who,obj,"摆摊一键取回",None)

	sendStallItem(who)

def rpcStallOneKeyGetMoney(who, reqMsg):
	'''一键提现
	'''
	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	if not itemObj:
		return

	priceAll = 0
	for itemNo in xrange(1,itemObj.count+1):
		price = itemObj.removePrice(itemNo)
		priceAll += price

	if not priceAll:
		return

	who.rewardTradeCash(priceAll,"摆摊一键提现",None)
	message.tips(who,"成功提现#R<{},2,2>#n".format(priceAll))
	sendStallItem(who)
	listener.doListen("摆摊提现", who, cash=priceAll)

def rpcStallBuyItem(who, reqMsg):
	'''购买摊位
	'''
	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	if not itemObj:
		itemObj = trade.gStall.addStallItem(who.id)
	count = itemObj.count
	cost = tradeGoodsData.gdStallExtend.get(count+1,{}).get("费用",0)
	if not cost:
		return
	if who.tradeCash < cost:
		if not money.checkTradeCash(who,cost):
			return
		itemObj = trade.gStall.goodsListByRoleId.get(who.id)
		if not itemObj or itemObj.count != count:
			return

	who.costTradeCash(cost,"购买摊位","消耗#R<{},2,2>#n，摊位空间#C04+1#n".format(cost))
	itemObj.addCount(1)
	sendStallItem(who)

def rpcStallGetProps(who, reqMsg):
	'''下架物品
	'''
	itemNo = reqMsg.iValue
	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	if not itemObj or itemNo not in itemObj.goodsList:
		message.tips(who,"此商品已出售，无法取回")
		sendStallItem(who)
		return

	if not who.propsCtn.leftCapacity():
		message.tips(who,"包裹已满，无法取出")
		return

	stallId = itemObj.goodsList[itemNo]
	dGoods = trade.gStall.removeGoods(stallId,False)
	propsFork = props.fork(dGoods["obj"])
	launch.launchProps(who,propsFork,"下架物品:%s" % propsFork.id,None)
	msg = trade_pb2.sellItem()
	setStallItem(msg,itemObj,itemNo)
	who.endPoint.rpcStallItemMod(msg)

def rpcStallGetMoney(who, reqMsg):
	'''提取现金
	'''
	itemNo = reqMsg.iValue
	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	if not itemObj or itemNo not in itemObj.priceList:
		return
	price = itemObj.removePrice(itemNo)
	who.rewardTradeCash(price,"摆摊提取现金",None)
	message.tips(who,"成功提现#R<{},2,2>#n".format(price))
	sendStallItem(who)
	listener.doListen("摆摊提现", who, cash=price)

def rpcStallSellAgain(who, reqMsg):
	'''再次上架
	'''
	stallId = reqMsg.stallId
	price = reqMsg.price

	goodsObj = trade.gStall.getGoodsObj(stallId)
	if not goodsObj:
		message.tips(who,"此商品已出售，无法上架")
		sendStallItem(who)
		return

	stack = goodsObj.stack()
	priceAll = getStallPoundage(stack * price)
	if who.cash < priceAll:
		if not money.checkCash(who,priceAll):
			return
		goodsObj = trade.gStall.getGoodsObj(stallId)
		if not goodsObj:
			message.tips(who,"此商品已出售，无法上架")
			sendStallItem(who)
			return
		if goodsObj.stack() > stack:
			return
		priceAll = getStallPoundage(goodsObj.stack() * price)

	itemNo = trade.gStall.getGoodsItemNo(stallId)
	who.costCash(priceAll,"摆摊重新上架",None)
	trade.gStall.removeGoods(stallId,False)
	trade.gStall.addGoods(who.id,goodsObj,price,itemNo=itemNo)

	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	msg = trade_pb2.sellItem()
	setStallItem(msg,itemObj,itemNo)
	who.endPoint.rpcStallItemMod(msg)
	who.endPoint.rpcStallSellSuccess(trade.getGoodsNo(goodsObj))

def rpcStallSearch(who, reqMsg):
	'''寻找商品
	'''
	goodsNo = reqMsg.iValue
	if not trade.gStall.getGoodCountByType(goodsNo):
		who.endPoint.rpcStallSearchNone(goodsNo)
		return
	sendStallList(who, goodsNo,2)

def openStall(who, goodsNo, taskId):
	'''打开摆摊
	'''
	msg = getStallListMsg(who,goodsNo,taskId=taskId)
	who.endPoint.rpcOpenStall(**msg)

def sendStallList(who, goodsNo, fromType=1, order=1, page=1, taskId=0):
	'''发送摆摊列表
	'''
	msg = getStallListMsg(who,goodsNo,fromType,order,page)
	who.endPoint.rpcStallList(**msg)

def getStallListMsg(who, goodsNo, fromType=1, order=1, page=1, taskId=0):
	'''获取摆摊列表信息
	'''
	goodsList = trade.gStall.getGoodListByType(goodsNo)
	msg = {}
	pageMax = (len(goodsList)+8-1)/8
	if page > pageMax :
		msg["pageMax"] = pageMax
	else:
		if order == 1:    #顺序
			start = (page-1)*8
			end = min(start+8,len(goodsList))
			step = 1
		else:
			start = len(goodsList) - ((page-1)*8) - 1
			end = start-8 if start-8>=-1 else None
			step = -1

		msg["pageMax"] = pageMax
		msg["order"] = order
		msg["page"] = page
		msg["from"] = fromType
		msg["stallList"] = [packStallProps(stallId) for stallId in goodsList[start:end:step]]
		msg["taskId"] = taskId

	return msg

def checkStallBuy(who,stallId,count,goodsNo):
	'''检查购买条件
	'''
	if not count:
		return False

	if trade.gStall.getGoodsSeller(stallId) == who.id:
		message.tips(who,"不能购买自己出售的物品")
		return

	goodsObj = trade.gStall.getGoodsObj(stallId)
	if not goodsObj or goodsObj.stack() < count:
		message.tips(who,"该物品信息已发生变化，请重新选择物品。")
		sendStallList(who, goodsNo)
		return False

	if (count+goodsObj.maxStack()-1)/goodsObj.maxStack() > who.propsCtn.leftCapacity():
		message.tips(who,"包裹已满，无法购买")
		return False

	return True

def packStallProps(stallId):
	'''打包摆摊物品信息
	'''
	goodsObj = trade.gStall.getGoodsObj(stallId)
	goodsId = trade.getGoodsNo(goodsObj)

	msg = trade_pb2.stallProps()
	msg.stallId = stallId
	msg.goodsId = goodsId
	msg.count = goodsObj.stack()
	msg.price = trade.gStall.getGoodsPrice(stallId)
	msg.sellerId = trade.gStall.getGoodsSeller(stallId)
	msg.basePrice = int(trade.gTradeCashTradeCenter.getItem(goodsId).getPrice())
	if hasattr(goodsObj,"quality"):
		msg.quality = goodsObj.quality

	return msg

def sendStallItem(who):
	'''发送摊位信息
	'''
	itemObj = trade.gStall.goodsListByRoleId.get(who.id)
	if not itemObj:
		who.endPoint.rpcStallSellItem(trade.stall.INIT_COUNT)
		return

	msg = trade_pb2.sellItemList()
	msg.countMax = itemObj.count
	msg.iPriceAll = itemObj.getPriceAll()
	
	for itemNo in xrange(1,itemObj.count+1):
		if itemNo not in itemObj.priceList and itemNo not in itemObj.goodsList:
			continue
		obj = msg.itemList.add()
		setStallItem(obj,itemObj,itemNo)

	who.endPoint.rpcStallSellItem(msg)

def setStallItem(obj,itemObj,itemNo):
	'''设置摊位信息
	'''
	obj.itemNo = itemNo
	if itemNo in itemObj.goodsList:
		stallId = itemObj.goodsList[itemNo]
		obj.status = trade.gStall.goodsList[stallId]["status"]
		if obj.status == 1:
			obj.time = trade.gStall.getDownShelfTime(stallId)-getSecond()
		obj.porps.CopyFrom(packStallProps(stallId))
	else:
		obj.status = 0
	if itemNo in itemObj.priceList:
		obj.profit = itemObj.priceList[itemNo]

def getStallPoundage(cost):
	'''摆摊手续费
	'''
	if cost < 1000:
		cost = 1000
	elif cost > 1000000:
		cost = 100000
	return cost

def sendTradeMail(roleId, name, count, price):
	title = "交易成功"
	content = "恭喜，你成功出售了#C07{}×{}#n，获得#R<{},2,2>#n，快去提现吧！".format(name,count,price)
	mail.sendTradeMail(roleId,title, content,"")

from common import *
import tradeGoodsData
import trade
import message
import money
import launch
import props
import mail
import listener