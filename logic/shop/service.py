#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import shop_pb2
import endPoint

def handleLock(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		import role.roleConfig
		if role.roleConfig.isLock(who):
			who.endPoint.rpcSecurityUnlock()
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			raise
	return newFunc

#商店相关服务
class cService(shop_pb2.terminal2main):
	@endPoint.result
	def rpcBuyGoods(self,ep,who,reqMsg):return rpcBuyGoods(who,reqMsg)#购买商品

	@endPoint.result
	def rpcPropsExchange(self, ep, who, reqMsg):return rpcPropsExchange(who, reqMsg)

	@endPoint.result
	def rpcMoneyExchange(self, ep, who, reqMsg):return rpcMoneyExchange(who, reqMsg)

	@endPoint.result
	def rpcExchangeInfoReq(self, ep, who, reqMsg):return rpcExchangeInfoReq(who, reqMsg)

	@endPoint.result
	def rpcMallInfoReq(self, ep, who, reqMsg):return rpcMallInfoReq(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcMallBuy(self, ep, who, reqMsg):return rpcMallBuy(who, reqMsg)


def rpcBuyGoods(who,reqMsg):
	iPropsNo,iAmount = reqMsg.iPropsNo,reqMsg.iAmount
	if iAmount <= 0:
		message.tips(who, "购买数量异常")
		return
	if not shopData.hasProps(iPropsNo):
		return

	iNeedLv = shopData.getConfig(iPropsNo,"等级限制",-1)  #-1为没有等级限制
	# 人物>=40级只能买40级的物品，<40级只能买相关等级段的物品
	decimalLv = min(who.level/10*10, 40)
	if iNeedLv!=-1 and decimalLv != iNeedLv:
		message.tips(who, "等级不符合")
		return

	oProps = props.getCacheProps(iPropsNo)
	if not oProps:
		message.tips(who, "没有该物品")
		return

	iPrice = oProps.getConfig("出售价格")
	if iPrice <= 0:
		raise PlannerError("{}商品价格异常！请通知策划！".format(iPropsNo))
	iTotlePrice = iPrice*iAmount
	if not money.checkCash(who, iTotlePrice):
		return
	iCapacity = int(math.ceil(float(iAmount) / oProps.maxStack()))
	if iCapacity > who.propsCtn.leftCapacity():
		message.tips(who, "包裹已满，请清理包裹")
		return

	iBind = oProps.isBind()
	who.addCash(-iTotlePrice,"商店购买商品",None)
	launch.launchBySpecify(who,iPropsNo,iAmount,iBind,sLogReason="商店购买商品",sTips=None)
	message.tips(who, "成功购买了#C02{}#n件#C02{}#n".format(iAmount,oProps.name))
	
	import listener
	listener.doListen("购买物品", who, price=iPrice)

def rpcExchangeInfoReq(who, reqMsg):
	'''请求兑换信息
	'''
	iPointID = reqMsg.iPointID
	msg = shop.pointsShop.packShopInfo(who, iPointID)
	if not msg:
		return
	who.endPoint.rpcExchangeInfoRespone(msg)

def rpcPropsExchange(who, reqMsg):
	'''积分兑换物品
	'''
	iPointID = reqMsg.iPointID
	buyInfo = reqMsg.buyInfo
	iPropsNo = buyInfo.iPropsNo
	iAmount = buyInfo.iAmount
	if iAmount <= 0:
		message.tips(who, "购买数量异常")
		return
	shop.pointsShop.propsExchange(who, iPointID, iPropsNo, iAmount)
	msg = shop.pointsShop.packShopInfo(who, iPointID)
	who.endPoint.rpcExchangeInfoRespone(msg)

def rpcMoneyExchange(who, reqMsg):
	'''货币之间相互兑换
	'''
	iMoneyType = reqMsg.iMoneyType
	iSource = reqMsg.iSource
	iAmount = reqMsg.iAmount
	if iMoneyType not in (1, 2,):
		message.tips(who, "目前只能兑换银币和元宝")
		return
	if iAmount < 0:
		return
	if iMoneyType == 1:
		if iSource not in (2, 3,):
			message.tips(who, "银币只能通过元宝或龙纹玉来兑换")
			return
		if iSource == 2 and iAmount <= 9999999:
			money.tradeCash2Cash(who, iAmount)
		elif iSource == 3 and iAmount <= 99999:
			money.moneyCash2Cash(who, iAmount)
	elif iMoneyType == 2:
		if iSource != 3:
			message.tips(who, "元宝只能通过龙纹玉来兑换")
			return
		if iAmount > 99999:
			return
		money.moneyCash2TradeCash(who, iAmount)
	common.writeLog("shop/moneyExchange", "{}({}) {}->{} {}".format(who.name, who.id, iSource, iMoneyType, iAmount))

def rpcMallInfoReq(who, reqMsg):
	'''请求商城信息
	'''
	iMallType = reqMsg.iMallType
	msg = shop.mall.packMallInfo(who, iMallType)
	if not msg:
		return
	who.endPoint.rpcMallInfoRespone(msg)

def rpcMallBuy(who, reqMsg):
	'''购买商城物品
	'''
	iMallType = reqMsg.iMallType
	buyInfo = reqMsg.mallProps[0]
	iPropsNo = buyInfo.iPropsNo
	iAmount = buyInfo.iAmount
	if iAmount <= 0:
		message.tips(who, "购买数量异常")
		return
	shop.mall.mallBuy(who, iMallType, iPropsNo, iAmount)
	msg = shop.mall.packMallInfo(who, iMallType)
	who.endPoint.rpcMallInfoRespone(msg)


import math
import shopData
import equipData
import propsData
import launch
import props
import money
import message
import shop.pointsShop
import shop.mall
import common
