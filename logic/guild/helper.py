#-*-coding:utf-8-*-



def getLastContributeDay(iLastContri):
	iDayNo=timeU.getDayNo()
	if iLastContri==-1:
		return ''
	elif iLastContri==iDayNo:
		return '今天'
	elif iDayNo-iLastContri==1:
		return '昨天'
	elif iDayNo-iLastContri==2:
		return '两天前'
	elif iDayNo-iLastContri==3:
		return '三天前'
	elif iDayNo-iLastContri==4:
		return '四天前'
	elif iDayNo-iLastContri==5:
		return '五天前'
	elif iDayNo-iLastContri==6:
		return '六天前'
	elif iDayNo-iLastContri<=13:
		return '一周前'
	elif iDayNo-iLastContri<=20:
		return '两周前'
	elif iDayNo-iLastContri<=27:
		return '三周前'
	elif iDayNo-iLastContri<=30:
		return '四周前'
	else:
		return '一个月以上'

import timeU
import guild