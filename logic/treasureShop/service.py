# -*- coding: utf-8 -*-
# 交易中心服务
import endPoint
import treasureShop_pb2

class cService(treasureShop_pb2.terminal2main):

	@endPoint.result
	def rpcTSGoodsListReq(self, ep, who, reqMsg): return rpcGoodsListReq(who, reqMsg)
	
	@endPoint.result
	def rpcTSGoodsInfoReq(self, ep, who, reqMsg): return rpcGoodsInfoReq(who, reqMsg)
	
	@endPoint.result
	def rpcTSGoodsBuy(self, ep, who, reqMsg): return rpcGoodsBuy(who, reqMsg)
	
	@endPoint.result
	def rpcTSGoodsSell(self, ep, who, reqMsg): return rpcGoodsSell(who, reqMsg)

	@endPoint.result
	def rpcTSGoodsSellAgain(self, ep, who, reqMsg): return rpcGoodsSellAgain(who, reqMsg)

	@endPoint.result
	def rpcTSGoodsGetBack(self, ep, who, reqMsg): return rpcTSGoodsGetBack(who, reqMsg)

	@endPoint.result
	def rpcTSGoodsAttentionSet(self, ep, who, reqMsg): return rpcGoodsAttentionSet(who, reqMsg)

	@endPoint.result
	def rpcTSItemLisReq(self, ep, who, reqMsg): return rpcItemLisReq(who, reqMsg)

	@endPoint.result
	def rpcTSProfitGet(self, ep, who, reqMsg): return rpcProfitGet(who, reqMsg)

	@endPoint.result
	def rpcTSGoodsReport(self, ep, who, reqMsg): return rpcGoodsReport(who, reqMsg)

def rpcGoodsListReq(who, reqMsg):
	'''物品列表请求
	'''
	iGoodsId = reqMsg.iGoodsId
	iOrder = reqMsg.iOrder
	iPage = reqMsg.iPage
	iType = reqMsg.iType

	rpcGoodsListSend(who,iGoodsId,iOrder,iPage,iType)

def rpcGoodsInfoReq(who, reqMsg):
	'''物品请求
	'''
	iStallId = reqMsg.iStallId
	iGoodsId = reqMsg.iGoodsId
	iType = reqMsg.iType
	if iType == 3:
		dGoods = treasureShop.gReportBoard.getGoods(iStallId)
		if not dGoods:
			message.tips(who,"物品已经过了7天审核期")
			rpcGoodsListSend(who,iGoodsId,1,1,iType)
			return 
	else:
		dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
		if not dGoods:
			message.tips(who,"物品已下架或被人购买")
			rpcGoodsListSend(who,iGoodsId,1,1,iType)
			return
	rpcGoodsSend(who,iStallId)

def rpcGoodsBuy(who, reqMsg):
	'''购买物品
	'''
	if who.level < 40:
		return
	iStallId = reqMsg.iStallId
	iGoodsId = reqMsg.iGoodsId
	dGoods = checkBuyCondition(who, iStallId)
	if not dGoods:
		rpcGoodsListSend(who,iGoodsId,1,1,1)
		return
	iPrice = dGoods["price"]
	if who.tradeCash < iPrice:
		if not money.checkTradeCash(who,iPrice):
			return
		dGoods = checkBuyCondition(who, iStallId)
		if not dGoods:
			rpcGoodsListSend(who,iGoodsId,1,1,1)
			return

	oProps = dGoods["obj"]
	treasureShop.gTreasureShop.updateStatus(iStallId,treasureShop.object.SELL_CHECK)
	who.addTradeCash(-iPrice,"珍品阁购买",None)
	message.tips(who,"花费#R<{},2,2>#n，获得#C02{}×1#n".format(iPrice,oProps.name))
	oPropsFork = props.fork(oProps)
	oPropsFork.setStallCD(getDayNo()+30)
	writeLog("treasureShop/buy","玩家%s购买物品(id:%d,name:%s,price:%d)" % (who.id,oPropsFork.id,oPropsFork.name,iPrice))
	launch.launchProps(who,oPropsFork,"珍品阁购买","花费#R<%d,2,2>#n，获得%s X 1" % (iPrice,oProps.name))
	sendMailToSeller(dGoods)

	oProps4Board = props.fork(oPropsFork)
	treasureShop.gReportBoard.addGoods(dGoods["ownerId"],oProps4Board,iPrice,who.id,[],[])
	iGoodsId = treasureShop.getGoodsNo(oProps)
	rpcGoodsListSend(who,iGoodsId,1,1,1)

	listener.doListen("购买珍品", who, price=iPrice)
	

def rpcGoodsSell(who, reqMsg):
	'''上架物品
	'''
	if who.level < 40:
		return
	iPropsId = reqMsg.iPropsId
	iPrice = reqMsg.iPrice
	if not 10000 <= iPrice < 10000000000:
		return

	oProps = checkProps(who,iPropsId)
	if not oProps:
		message.tips(who,"你要上架的物品已被购买或消失，无法上架")
		return

	if oProps.getStallCD():
		return

	iPoundage = getPoundage(iPrice)
	if who.cash < iPoundage:
		if not money.checkCash(who,iPoundage):
			return
		oProps = checkProps(who,iPropsId)
		if not oProps:
			message.tips(who,"你要上架的物品已被购买或消失，无法上架")
			return

	who.addCash(-iPoundage,"上架物品",None)
	oPropsFork = getGoodsFork(oProps)
	removeProps(who,oProps)
	iStallId = treasureShop.gTreasureShop.addGoods(who.id,oPropsFork,iPrice,[])
	message.tips(who,"上架成功")
	writeLog("treasureShop/sell","玩家%s上架物品(id:%d,name:%s,price:%d)" % (who.id,oProps.id,oProps.name,iPrice))
	who.endPoint.rpcTSItemMod(packItemInfo(who,iStallId,getSecond()))
	who.endPoint.rpcTSSellSuccess(treasureShop.getGoodsNo(oProps))

def rpcGoodsSellAgain(who, reqMsg):
	'''再次上架物品
	'''
	if who.level < 40:
		return
	iStallId = reqMsg.iStallId
	print iStallId
	iPrice = reqMsg.iPrice
	if not 10000 <= iPrice < 10000000000:
		return
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods:
		message.tips(who,"你要上架的物品已被购买或消失，无法上架")
		return
	iPoundage = getPoundage(iPrice)
	if who.cash < iPoundage:
		if not money.checkCash(who,iPoundage):
			return
		dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
		if not dGoods:
			message.tips(who,"你要上架的物品已被购买或消失，无法上架")
			return

	who.addCash(-iPoundage,"再上架物品",None)
	oProps = dGoods["obj"]
	treasureShop.gTreasureShop.removeGoods(iStallId)
	iStallId = treasureShop.gTreasureShop.addGoods(who.id,oProps,iPrice,[])
	writeLog("treasureShop/sell","玩家%s再次上架物品(id:%d,name:%s,price:%d)" % (who.id,oProps.id,oProps.name,iPrice))
	who.endPoint.rpcTSItemMod(packItemInfo(who,iStallId,getSecond()))
	who.endPoint.rpcTSSellSuccess(treasureShop.getGoodsNo(oProps))

def rpcTSGoodsGetBack(who, reqMsg):
	'''取回物品
	'''
	iStallId = reqMsg.iStallId
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods or dGoods["status"] == treasureShop.object.SELL_CHECK:
		message.tips(who,"你要取回的物品已被购买或消失，无法上架")
		rpcItemListSend(who)
		return
	if not who.propsCtn.leftCapacity():
		message.tips(who,"背包空间不足，不能取回")
		return

	dGoods = treasureShop.gTreasureShop.removeGoods(iStallId)
	oPropsFork = props.fork(dGoods["obj"])
	launch.launchProps(who,oPropsFork,"珍品阁取回物品",None)
	who.endPoint.rpcTSItemDel(dGoods["itemId"])
	writeLog("treasureShop/back","玩家%s取回上架物品(id:%d,name:%s)" % (who.id,oPropsFork.id,oPropsFork.name))

def rpcGoodsAttentionSet(who, reqMsg):
	'''设置关注
	'''
	if who.level < 40:
		return
	iStallId = reqMsg.iStallId
	bAttention = reqMsg.bAttention
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods:
		message.tips(who, "物品已下架或被人购买")
		return
	treasureShop.gTreasureShop.setAttention(who.id,iStallId,bAttention)
	rpcGoodsInfoMod(who,iStallId,"iAttention","bAttention")

def rpcItemLisReq(who, reqMsg):
	'''摊位列表请求
	'''
	rpcItemListSend(who)

def rpcProfitGet(who, reqMsg):
	'''提取现金
	'''
	iStallId = reqMsg.iStallId
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods or dGoods["status"] != treasureShop.object.SELL_MONEY:
		return
	treasureShop.gTreasureShop.removeGoods(iStallId)
	iPrice = dGoods["price"]
	who.addTradeCash(iPrice,"摆摊提取现金",None)
	message.tips(who,"成功提现#R<%d,2,2>#n" % iPrice)
	who.endPoint.rpcTSItemDel(dGoods["itemId"])
	who.endPoint.rpcTSItemListMod(treasureShop.gTreasureShop.getPrice(who.id))

def rpcGoodsReport(who, reqMsg):
	'''举报
	'''
	if who.level < 40:
		return
	iStallId = reqMsg.iStallId
	dGoods = treasureShop.gReportBoard.getGoods(iStallId)
	if not dGoods or iStallId in treasureShop.gReportBoard.getReportList(who.id):
		message.tips(who,"你已举报过此物品")
		return
	iHuoli = int(dGoods["price"] * 15 /10000) - 10
	iHuoli = max(10,min(iHuoli,100))
	if who.huoli < iHuoli:
		message.tips(who,"你的活力不足，不能举报")
		return
	who.addHuoli(-iHuoli,"举报物品",None)
	treasureShop.gReportBoard.addReport(iStallId,who)
	rpcGoodsInfoMod(who,iStallId,"iReport","bReport")
	message.tips(who,"举报成功")

def rpcGoodsListSend(who, iGoodsId, iOrder, iPage, iType):
	'''发送物品列表
	'''
	if iType == 3:
		if not iGoodsId:
			goodsList = treasureShop.gReportBoard.getReportList(who.id)
		else:
			goodsList = treasureShop.gReportBoard.getGoodList(iGoodsId)
	else:
		if not iGoodsId:
			goodsList = treasureShop.gTreasureShop.getAttentionList(iType,who.id)
		else:
			goodsList = treasureShop.gTreasureShop.getGoodList(iType,iGoodsId)
	msg = {}
	msg["iGoodsId"] = iGoodsId
	msg["iOrder"] = iOrder
	msg["iPage"] = iPage
	msg["iType"] = iType

	iPageMax = (len(goodsList)+8-1)/8
	if iPageMax and iPage <= iPageMax :
		if iOrder == 1:    #顺序
			iStart = (iPage-1)*8
			iEnd = min(iStart+8,len(goodsList))
			iStep = 1
		else:
			iStart = len(goodsList) - ((iPage-1)*8) - 1
			iEnd = iStart-8 if iStart-8>=-1 else None
			iStep = -1

		msg["iPageMax"] = iPageMax
		msg["goodsList"] = [packGoodsInfo(who,iStallId) for iStallId in goodsList[iStart:iEnd:iStep]]

	who.endPoint.rpcTSGoodsListSend(**msg)

def rpcGoodsSend(who,iStallId):
	'''发送物品
	'''
	who.endPoint.rpcTSGoodsInfoSend(packGoodsInfo(who,iStallId,False))

def rpcGoodsInfoMod(who,iStallId,*attrList):
	'''物品信息修改
	'''
	msg = {}
	msg["iStallId"] = iStallId
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods:
		dGoods = treasureShop.gReportBoard.getGoods(iStallId)
	for attr in attrList:
		if attr == "iAttention":
			msg[attr] = len(dGoods["attention"])
		elif attr == "bAttention":
			msg[attr] = who.id in dGoods["attention"]
		elif attr == "iReport":
			msg[attr] = len(dGoods["vReport"]) + len(dGoods["ivReport"])
		elif attr == "bReport":
			msg[attr] = iStallId in treasureShop.gReportBoard.getReportList(who.id)

	who.endPoint.rpcTSGoodsInfoMod(**msg)

def rpcItemListSend(who):
	'''发送摊位列表
	'''
	lst = []
	iNow = getSecond()
	for iStallId in treasureShop.gTreasureShop.getRoleItem(who.id).itervalues():
		oMsg = packItemInfo(who, iStallId, iNow)
		lst.append(oMsg)
	
	msg = {}
	msg["iPriceAll"] = treasureShop.gTreasureShop.getPrice(who.id)
	msg["itemList"] = lst

	who.endPoint.rpcTSItemListSend(**msg)

def packItemInfo(who, iStallId, iNow):
	'''打包摊位信息
	'''
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	oMsg = treasureShop_pb2.itemInfo()
	oMsg.iItemId = dGoods["itemId"]
	oMsg.iStatus = dGoods["status"]
	oMsg.goodsInfo.CopyFrom(packGoodsInfo(who,iStallId))
	if dGoods["status"] in (1,2,4):
		oMsg.iTime = treasureShop.gTreasureShop.getShowTime(iStallId,iNow)

	return oMsg

def packGoodsInfo(who, iStallId, bFirst=True):
	'''打包物品信息
	'''
	oMsg = treasureShop_pb2.goodsInfo()
	oMsg.iStallId = iStallId

	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if dGoods:
		oMsg.iPrice = dGoods["price"]
		oMsg.iGoodsId = treasureShop.getGoodsNo(dGoods["obj"])
		oMsg.iAttention = len(dGoods["attention"])
		oMsg.bAttention = who.id in dGoods["attention"]
		oMsg.iSellerId = dGoods["ownerId"]
		iStatus = dGoods["status"]
		if iStatus in (1,2):
			oMsg.iType = iStatus
			oMsg.iTime = treasureShop.gTreasureShop.getShowTime(iStallId,getSecond())
	else:
		dGoods = treasureShop.gReportBoard.getGoods(iStallId)
		oMsg.iPrice = dGoods["price"]
		oMsg.iGoodsId = treasureShop.getGoodsNo(dGoods["obj"])
		oMsg.iReport = len(dGoods["vReport"]) + len(dGoods["ivReport"])
		oMsg.bReport = iStallId in treasureShop.gReportBoard.getReportList(who.id)
		oMsg.iTime = treasureShop.gReportBoard.getDownTime(iStallId) - getSecond()
		oMsg.iSellerId = dGoods["ownerId"]
	if not bFirst:
		dGoods["obj"].setTreasureShopMsg(oMsg)

	return oMsg

def checkBuyCondition(who, iStallId):
	'''检查购买条件
	'''
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods:
		message.tips(who,"物品已下架或被人购买")
		return {}
	if who.id == dGoods["ownerId"]:
		message.tips(who,"不能购买自己上架的物品")
		return {}
	if not who.propsCtn.leftCapacity():
		message.tips(who,"背包空间不足，不能购买")
		return {}
	if dGoods["status"] != treasureShop.object.SELL_ING:
		message.tips(who,"物品已下架或被人购买")
		return {}
	return dGoods

def checkProps(who,iPropsId):
	'''检查物品
	'''
	oProps = who.propsCtn.getItem(iPropsId)
	if oProps:
		iGoodsId = treasureShop.getGoodsNo(oProps)
		if iGoodsId not in treasureShopData.gdTreasureShopData:
			return None
		if not oProps.isRare():
			return None
		if oProps.gems():
			return None
	else:
		oProps = who.eyeCtn.getItem(iPropsId)

	freeItemId = treasureShop.gTreasureShop.getFreeItemId(who.id)
	if not freeItemId:
		return None

	return oProps

def getGoodsFork(obj):
	'''拷贝
	'''
	if isinstance(obj,props.equip.cProps):
		goodsFork = props.fork(obj)
	else: #物品
		goodsFork = props.new(obj.no())
		eyeFork = lineup.forkEye(obj)
		goodsFork.setEye(eyeFork)
	return goodsFork

def removeProps(who,obj):
	'''移除物品
	'''
	if isinstance(obj,props.equip.cProps):
		who.propsCtn.addStack(obj,-1)
	else:
		who.eyeCtn.removeItem(obj)

def getPoundage(cost):
	'''手续费
	'''
	return min(cost * 10,100000)

def sendMailToSeller(dGoods):
	'''发送邮件
	'''
	iSellerId = dGoods["ownerId"]
	iPrice = dGoods["price"]
	obj = dGoods["obj"]
	iItemId = dGoods["itemId"]
	link = "#L2<{},{},{},{}>*[{}]*02#n".format(iSellerId,11,obj.no(),iItemId,obj.name)
	if dGoods["status"] == 4:
		sContent = "亲爱的玩家，你出售的{}已被其他玩家购买，你获得了#R<{},2,2>#n，通过24小时审核后即可从珍品阁出售界面提现".format(link,iPrice)
	else:
		sContent = "亲爱的玩家，你出售的{}已被其他玩家购买，你可从珍品阁出售界面进行提现".format(link)
	mail.sendTradeMail(iSellerId,"珍品阁出售",sContent)

from common import *
import treasureShop
import treasureShop.object
import treasureShopData
import message
import money
import launch
import props
import mail
import lineup
import props.equip
import listener