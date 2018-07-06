# -*- coding: utf-8 -*-

def autoHolidayTask(who):
	holidayId = holidayData.getCurrentHoliday()
	if not holidayId:
		return
	taskObj = task.hasTask(who,10001)
	if taskObj or holiday.isTakeGift(who, holidayId):
		return
	levelLimit = holidayData.getConfig(holidayId, "领取等级")
	if who.level < levelLimit:
		return
		
	task.newTask(who, None, 10001)

import holidayData
import task
import holiday