#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇
#time util,时间相关的工具函数
import time

gtStandardTime=(2013,10,21,0,0,0,0,0,0)
giStandardTime=int(time.mktime(gtStandardTime))

#从1970年1月1日8点至今经过的秒数
def getStamp():#当前时间戳,秒为单位,整形
	return int(gevent.core.time())
	#return int(time.time())

	#在windows下测试:
	#gevent.core.time()比time.time()执行效率快一点点
	#gevent.core.time()精度更高,小数点后最多有6位
	#time.time()精度低一点,小数点后最多有3位

#今天的起始时间戳，秒数
def todDayStartStamp(i=0):
	if i==0:
		i=getStamp()
	t=time.localtime(i)
	return int(time.mktime((t[0],t[1],t[2],0,0,0,0,0,t[8]))) #t[8]是否是夏令时之类的

#下一天距离现在多少秒
def howManySecondNextDay(i=0):
	if i==0:
		i=getStamp()
	t=time.localtime(i)
	#直接对day加1,即使当前是月尾最后一天,也不会有问题
	return int(time.mktime((t[0],t[1],t[2]+1,0,0,0,0,0,t[8])))-i #t[8]是否是夏令时之类的

#下一小时距离现在多少秒
def howManySecondNextHour(i=0):
	if i==0:
		i=getStamp()
	t=time.localtime(i)
	#直接对hour加1,即使当前是23点,也不会有问题
	return int(time.mktime((t[0],t[1],t[2],t[3]+1,0,0,0,0,t[8])))-i #t[8]是否是夏令时之类的

#下一周距离现在多少秒
def howManySecondNextWeek(i=0):
	if i==0:
		i=getStamp()
	t=time.localtime(i)
	iDay=6-t[6]
	return int(time.mktime((t[0],t[1],t[2]+1,0,0,0,0,0,t[8])))-i+iDay*24*60*60

#下一月距离现在多少秒
def howManySecondNextMonth(i=0):
	if i==0:
		i=getStamp()
	t=time.localtime(i)
	#直接对month加1,即使当前是12月,也不会有问题
	return int(time.mktime((t[0],t[1]+1,1,0,0,0,0,0,t[8])))-i #t[8]是否是夏令时之类的

def getMinuteNo(i=0):#时间戳,分钟序号,从1开始
	if not i:
		i=getStamp()
	return (i-giStandardTime)/60+1
	#return (i-giStandardTime)/5+1

def getHourNo(i=0):#时间戳,小时序号,从1开始
	if not i:
		i=getStamp()
	return (i-giStandardTime)/3600+1

def getDayNo(i=0):#时间戳,天序号,从1开始
	if not i:
		i=getStamp()
	return (i-giStandardTime)/3600/24+1

def getWeekNo(i=0):#时间戳,周序号,从1开始
	if not i:
		i=getStamp()
	return (i-giStandardTime)/3600/24/7+1

def getMonthNo(i=0):#时间戳,月序号,从1开始
	# if not i:
	# 	i=getStamp()
	# return (i-giStandardTime)/(5*31)+1

	if not i:
		i=getStamp()
	tTime=time.localtime(i)
	#仅仅是月份相减,有可能会是负数,要考虑到年的变化因素
	return (tTime[0]-gtStandardTime[0])*12+(tTime[1]-gtStandardTime[1])+1

def getMaintainNo(i=0, w=1, h=8, mi=0):#时间戳，维护周序号，年*100+周
	# Monday is 0 在指定星期w,小时h,分钟mi前都是上一周，指定时间后为新的一周
	if not i:
		i=getStamp()
	tm = time.localtime(i)
	iWyear = int(time.strftime("%W", tm))
	iYear = tm.tm_year
	if tm.tm_wday < w or tm.tm_hour < h or tm.tm_min < mi:
		iWyear -= 1
	if iWyear < 0:
		iYear -= 1
		# 上一年的最后一周
		tm2 = time.strptime("31 12 %d" % iYear, "%d %m %Y")
		iWyear = int(time.strftime("%W", tm2))
	return iYear * 100 + iWyear

#返回时间文本，such as  94天21时56分5秒
def getTimeStr(i):
	iDay=i/(24*3600)
	iHour=i%(24*3600)/3600
	iMin=i%(3600*24)%3600/60
	iSec=i%60

	l=[]
	if iDay:
		l.append('{}天'.format(iDay))
	if iHour:
		l.append('{}小时'.format(iHour))
	if iMin:
		l.append('{}分钟'.format(iMin))
	if iSec:
		l.append('{}秒'.format(iSec))
	return ''.join(l)

#由mysql datetime（'2012-10-25 15:04:51'）类型转换成python的
#时间戳,即是time.mktime((2012,10,25,15,4,51,0,0,0))后的结果
def str2stamp(sTime):#返回整形
	lResult=[]
	for sDesTime in sTime.split(' '):#清空分开
		sSplit=''
		if sDesTime.find('-') != -1:
			sSplit='-'
		elif sDesTime.find(':') != -1:
			sSplit=':'
		else:
			raise Exception,'mysql datetime转换错误.'
		for sDate in sDesTime.split(sSplit):
			lResult.append(int(sDate))

	while len(lResult) < 9:	#9个元素的元组
		lResult.append(0)
	return int(time.mktime(tuple(lResult)))

#跟上面的函数作用相反，转换getStamp()成'2012-10-25 15:4:51'
def stamp2str(fStamp=None):
	if fStamp==None:
		tResult=time.localtime()
	else:
		tResult=time.localtime(fStamp)
	return time.strftime('%Y-%m-%d %H:%M:%S',tResult)


def minuteNo2str(iMinuteNo):#分钟序号转为'2012-10-25 15:4:51'格式
	iStamp=(iMinuteNo-1)*60+giStandardTime
	return stamp2str(iStamp)

def dayNo2str(iDayNo):#时间序号转为'2012-10-25' 格式 并没有时分秒
	iStamp=(iDayNo-1)*24*60*60+giStandardTime
	tResult=time.localtime(iStamp)
	return time.strftime('%Y-%m-%d',tResult)

# def init(tStandardTime=(2013,10,21,0,0,0,0,0,0)):#	2013-10-21 (星期一)0点
# 	global gtStandardTime,giStandardTime
# 	gtStandardTime=tStandardTime
# 	giStandardTime=int(time.mktime(gtStandardTime))

def isFirstDayFromMonth():  #当天是否是当前月的第一天
	tTime=time.localtime(getStamp())
	return tTime[2]==1

def isNewMinute():
	tTime=time.localtime(getStamp())
	return tTime[5]==0

def isNewHour():
	tTime=time.localtime(getStamp())
	return tTime[4]==0

def isNewDay(iHour):
	tTime=time.localtime(getStamp())
	return tTime[3]==0

def getMonthNoAfter6am(i=0):
	if not i:
		i=getStamp()
	tTime=time.localtime(i)
	#仅仅是月份相减,有可能会是负数,要考虑到年的变化因素
	iMonthNo=(tTime[0]-gtStandardTime[0])*12+(tTime[1]-gtStandardTime[1])+1
	return iMonthNo-1 if tTime[2]==1 and tTime[3]<6 else iMonthNo

# def getDayNoAfter6am(i=0):
# 	if not i:
# 		i=getStamp()
# 	return (i-giStandardTimeAfter6am)/3600/24+1

import gevent.core

# giStandardTimeAfter6am=int(time.mktime((2013,10,21,6,0,0,0,0,0)))
