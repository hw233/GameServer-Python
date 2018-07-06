#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇
#关健时间点的事件
#整点事件
#整天事件
#整周事件
#整月事件

def onNewHour():
	global gDayNo
	global gWeekNo
	global gMonthNo
	global gTempTime
	
	if gTempTime is not None:
		seconds = getSecond()
	else:
		seconds = timeU.getStamp()

	t=time.localtime(seconds)
	year, month, day, hour = t[:4]
	wday = t[6]+1
	
	geNewHour(year,month,day,hour,wday)#触发事件

	#各事件参数为,年,月,日,时,星期几(1~7,星期日是7,因为我已经加了1,原本是0~6的)
	#日期变化，触发日事件
	if gDayNo!=timeU.getDayNo(seconds):
		gDayNo=timeU.getDayNo(seconds)
		geNewDay(year,month,day,hour,wday)#触发事件

	#周号变化，触发周事件
	if gWeekNo!=timeU.getWeekNo(seconds):
		gWeekNo=timeU.getWeekNo(seconds)
		geNewWeek(year,month,day,hour,wday)#触发事件

	#月份变化，触发月事件
	if gMonthNo!=timeU.getMonthNo(seconds):
		gMonthNo=timeU.getMonthNo(seconds)
		geNewMonth(year,month,day,hour,wday)#触发事件

def onNewMinum():
	geNewMinu()
	
import time
import u
import timeU
import timer
from common import *

if 'gbOnce' not in globals():
	gbOnce=True
	global geNewHour,geNewDay,geNewWeek,geNewMonth,geNewMinu
	global gDayNo,gWeekNo,gMonthNo
	global gTempTime
	
	geNewHour=u.cEvent()
	geNewDay=u.cEvent()
	geNewWeek=u.cEvent()
	geNewMonth=u.cEvent()
	geNewMinu=u.cEvent()

	gDayNo=timeU.getDayNo()
	gWeekNo=timeU.getWeekNo()
	gMonthNo=timeU.getMonthNo()
	gTempTime=None # 临时时间，用于指定时间的测试

	timer.gTimerMng.run(onNewHour,timeU.howManySecondNextHour(),3600,'onNewHour',None,timer.LOWEST)#启动定时器
	timer.gTimerMng.run(onNewMinum,0,60,'onNewMinu',None,timer.LOWEST)
