#coding:utf-8
'''
积分商店
{积分类型:{物品编号:限购数量}}
限购数量只是针对玩家个人，故限购信息应保存在个人数据中
dBuyInfo = who.week.fetch("pointsShop")#{积分类型:{物品编号:已购数量, ...}, ...}
'''
gdPointsIcon = {
200004:10,#降魔
200005:9,#门派
200006:11,#侠义
200007:12,#武勋
200010:14,#献花积分
}

def propsExchange(who, iPointID, iPropsNo, iAmount):
	'''兑换
	'''
	dPtProps = pointsExchangeData.getPropsByPointID(iPointID)
	dProps = dPtProps.get(iPropsNo)
	if not dProps:
		return
	if dProps.get("出现等级", 0) > who.level:
		message.tips(who, "你的等级不符合")
		return
	oProps = props.getCacheProps(iPropsNo)
	if not oProps:
		message.tips(who, "没有该物品")
		return
	iLimit = dProps.get("每周限购")
	if iLimit is None:
		message.tips(who, "该商店每周限购数量异常")
		return
	dPointShop = who.week.fetch("pointsShop", {})
	dBuyInfo = dPointShop.get(iPointID, {})
	iBuy = dBuyInfo.get(iPropsNo, 0)
	if iLimit != -1 and iAmount > (iLimit-iBuy):
		message.tips(who, "该商品在本周已售罄，请下周再继续购买")
		return
	iPrice = dProps.get("商品价格")
	if not iPrice:
		raise PlannerError,"没有填写编号为{}的商品价格".format(iPropsNo)
	iTotalPrice = iPrice*iAmount
	if getPoint(who, iPointID) < iTotalPrice:
		message.tips(who, "$P<{},1,1>#n不足，无法购买".format(gdPointsIcon[iPointID]))
		return
	iCapacity = int(math.ceil(float(iAmount) / oProps.maxStack()))
	if iCapacity > who.propsCtn.leftCapacity():
		message.tips(who, "背包空间不足，无法购买")
		return
	iBind = dProps.get("购买绑定", 0)
	addPoint(who, iPointID, -iTotalPrice)
	launch.launchBySpecify(who,iPropsNo,iAmount,iBind,sLogReason="商店购买商品",sTips=None)
	if not iBuy:
		dBuyInfo[iPropsNo] = iAmount
	else:
		dBuyInfo[iPropsNo] += iAmount
	dPointShop.update({iPointID:dBuyInfo})
	who.week.set("pointsShop", dPointShop)
	message.tips(who, "花费#C02{:,}#n$P<{},1,1>#n，获得#C02{}×{}#n".format(iTotalPrice, gdPointsIcon[iPointID], oProps.name, iAmount))
	common.writeLog("shop/pointsExchange", "{}({}) {}:{} {}:{}".format(who.name, who.id, iPointID, iTotalPrice, iPropsNo, iAmount))

def getPoint(who, iPointID):
	funcName = pointsExchangeData.pointHandler[iPointID]["get"]
	return getattr(who, funcName)

def addPoint(who, iPointID, val):
	funcName = pointsExchangeData.pointHandler[iPointID]["add"]
	func = getattr(who, funcName)
	func(val, "积分兑换")

def packShopInfo(who, iPointID):
	'''打包玩家指定类型的兑换商店信息
	'''
	msg = shop_pb2.exchangeInfo()
	msg.iPointID = iPointID
	lProps = []
	dBuyInfo = who.week.fetch("pointsShop", {}).get(iPointID, {})
	dSaleInfo = pointsExchangeData.getPropsByPointID(iPointID)
	if not dSaleInfo:
		return msg
	for idx, props in dSaleInfo.iteritems():
		propsMsg = shop_pb2.buyInfo()
		propsMsg.iPropsNo = idx
		iLimit = props.get("每周限购")
		iBuy = dBuyInfo.get(idx, 0)
		if iLimit != -1:
			iAmount = max(0, iLimit-iBuy)
		else:
			iAmount = -1
		propsMsg.iAmount = iAmount
		lProps.append(propsMsg)
	msg.buyInfo.extend(lProps)
	return msg


import math
import shop_pb2
import message
import pointsExchangeData
import props
import launch
import common
