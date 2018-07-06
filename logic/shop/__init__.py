# -*- coding: utf-8 -*-
'''
商店类相关
'''
import timerEvent
import shop.pointsShop

def newDay(iYear,iMonth,iDay,iHour,iWeek):
	shop.mall.init()

def init():
	shop.mall.init()
	
def openShop(who, npcIdx, taskId=0, propsNo=0, bShut=False):
	'''打开商店界面
	'''
	shopType = getShopTypeByNpcIdx(npcIdx)
	msg = {
		"iShopType" : shopType,
		"iTaskId" : taskId,
		"iPropsNo" : propsNo,
		"bShut" : bShut,
	}
	who.endPoint.rpcOpenShop(**msg)
	
def openPropsExchange(who, pointType):
	'''打开积分兑换界面
	'''
	who.endPoint.rpcOpenPropsExchange(pointType)
	
from shop.defines import *


if "gbOnce" not in globals():
	gbOnce=True
	timerEvent.geNewDay += newDay
