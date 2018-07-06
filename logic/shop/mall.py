# -*- coding: utf-8 -*-
'''
商城
# {商城类型:{商品编号:商品配置信息,...}...}
'''
if "gdMallProps" not in globals():
	gdMallProps = {}

def init():
	'''初始化商品
	'''
	global gdMallProps
	gdMallProps = {}
	for idx, cfg in mallData.gdData.iteritems():
		effDate = cfg.get("生效日期")
		if effDate and datetime.date(*effDate) > datetime.date.today():
			continue
		expireDate = cfg.get("失效日期")
		if expireDate and datetime.date(*expireDate) < datetime.date.today():
			continue
		cfg2 = dict(cfg)
		propsId = cfg.get("商品id")
		mallType = cfg.get("种类")
		cfg2["序号"] = idx # 客户端排序需要
		gdMallProps.setdefault(mallType, {}).update({propsId:cfg2})

def mallBuy(who, iMallType, iPropsNo, iAmount):
	'''购买商城物品
	'''
	if iMallType not in gdMallProps:
		message.tips(who, "没有该商城编号")
		return
	if iPropsNo not in gdMallProps[iMallType]:
		message.tips(who, "该商城没有此物品")
		return
	oProps = props.getCacheProps(iPropsNo)
	if not oProps:
		message.tips(who, "没有该物品")
		return
	dPropsInfo = gdMallProps[iMallType][iPropsNo]
	iLimit = dPropsInfo.get("每周限购")
	if iLimit is None:
		message.tips(who, "该商店每周限购数量异常")
		return
	dMall = who.week.fetch("mall", {})
	dBuyInfo = dMall.get(iMallType, {})
	iBuy = dBuyInfo.get(iPropsNo, 0)
	if iLimit != -1 and iAmount > (iLimit-iBuy):
		message.tips(who, "该商品在本周已售罄，请下周再继续购买")
		return
	iPrice = dPropsInfo.get("原价") * dPropsInfo.get("折扣") / 100
	if not iPrice:
		raise PlannerError,"没有填写编号为{}的折后价格".format(iPropsNo)
	iTotalPrice = iPrice*iAmount
	iCapacity = int(math.ceil(float(iAmount) / oProps.maxStack()))
	if iCapacity > who.propsCtn.leftCapacity():
		message.tips(who, "背包空间不足，无法购买")
		return
	pid = who.id
	if not money.checkMoneyCash(who, iTotalPrice):
		return
	who = common.getRole(pid)
	if not who:
		return
	who.addMoneyCash(-iTotalPrice, "商城购买商品", None)
	launch.launchBySpecify(who, iPropsNo, iAmount, False, sLogReason="商城购买商品",sTips=None)
	if not iBuy:
		dBuyInfo[iPropsNo] = iAmount
	else:
		dBuyInfo[iPropsNo] += iAmount
	dMall.update({iMallType:dBuyInfo})
	who.week.set("mall", dMall)
	message.tips(who, "花费#IX#n#C02{:,}#n，获得#C02{}×{}#n".format(iTotalPrice, oProps.name, iAmount))
	common.writeLog("shop/mall", "{}({}) {}:{} {}:{}".format(who.name, who.id, iMallType, iTotalPrice, iPropsNo, iAmount))

def packMallInfo(who, iMallType):
	'''打包玩家指定类型的商城信息
	'''
	msg = shop_pb2.mallInfo()
	msg.iMallType = iMallType
	if iMallType not in gdMallProps:
		return msg
	lProps = []
	dBuyInfo = who.week.fetch("mall", {}).get(iMallType, {})
	for propsId, cfg in gdMallProps[iMallType].iteritems():
		propsMsg = shop_pb2.mallProps()
		propsMsg.iPropsNo = propsId
		iLimit = cfg.get("每周限购", 0)
		iBuy = dBuyInfo.get(propsId, 0)
		iAmount = -1
		if iLimit != -1:
			iAmount = max(0, iLimit-iBuy)
		propsMsg.iAmount = iAmount
		propsMsg.iPrice = cfg.get("原价") * cfg.get("折扣") / 100
		propsMsg.iOriginal = cfg.get("原价")
		propsMsg.iWeight = cfg.get("权重")
		propsMsg.iIdx = cfg.get("序号")
		propsMsg.iTime = timeU.howManySecondNextWeek() if iMallType == 3 else -1
		lProps.append(propsMsg)
	msg.mallProps.extend(lProps)
	return msg


import datetime
import math
import shop_pb2
import mallData
import common
import props
import money
import message
import launch
import timeU
