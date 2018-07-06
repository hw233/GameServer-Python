# -*- coding: utf-8 -*-
'''节日礼物
'''

def isTakeGift(who, holidayId):
	'''是否已领取节日礼物
	'''
	holidayList = who.fetch("holiday", {})
	if not holidayList:
		return False
	
	val = holidayList.get(holidayId)
	valNew = getYearNo()
	if val == valNew:
		return True
	return False

def markTakeGift(who, holidayId):
	'''标记已领取节日礼物
	'''
	holidayList = who.fetch("holiday", {})
	val = getYearNo()
	holidayList[holidayId] = val
	who.set("holiday", holidayList)

from common import *