# -*- coding: utf-8 -*-

def getGoodsNo(obj):
	return obj.no()

def init():
	global gTreasureShop,gReportBoard
	gTreasureShop = treasureShop.object.cTreasureShop()
	if not gTreasureShop._loadFromDB():
		gTreasureShop._insertToDB(*gTreasureShop.getPriKey())

	gReportBoard = treasureShop.object.cReportBoard()
	if not gReportBoard._loadFromDB():
		gReportBoard._insertToDB(*gReportBoard.getPriKey())

def onLogin(who):
	iPriceAll = gTreasureShop.getPrice(who.id)
	who.endPoint.rpcTSItemListSend(iPriceAll)

import treasureShop.object