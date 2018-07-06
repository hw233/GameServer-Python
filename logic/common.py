# -*- coding: utf-8 -*-
# 此模块不要直接写业务逻辑代码，如getRole

def getRole(pid):
	import role
	return role.getRole(pid)

def getNpc(npcId):
	import npc
	return npc.getNpc(npcId)

def functor(func, *args, **kwargs):
	import u
	return u.cFunctor(func, *args, **kwargs)

def rand(n, m=None):
	'''随机数
	
	模式1: 0~n(不包含n)
	模式2: n~m(包含n和m)
	'''
	if m:
		if m == n:
			return m
		if m < n:
			m,n = n,m

	if not m:
		m = max(0, n - 1)
		n = 0
	return random.randint(n, m)

def shuffleList(lst, n=0):
	'''打乱一个列表
	'''
	if isinstance(lst, tuple):
		lst = list(lst)
	random.shuffle(lst)
	if n:
		return lst[:n]
	return lst

def chooseKey(data, total=0, key=None, filt=None):
	'''根据几率选出一项
	
	key: 指定哪一项是概率
	filt: 过滤函数
	'''
	if isinstance(data, (list, tuple)):
		data = {i:v for i,v in enumerate(data)}

	ratioList= {}
	for k,v in data.iteritems():
		if filt and not filt(k, v):
			continue
		if key:
			ratio = v[key]
		else:
			ratio = v
		ratioList[k] = ratio
	
	if total == 0:
		total = sum(ratioList.values())
	
	n = rand(total)
	m = 0
	for k,ratio in ratioList.iteritems():
		m += ratio
		if n < m:
			return k
	return None

'''
建议使用这里而不是timeU的getHourNo、getDayNo等方法，因为可以用于测试时间($testtime指令设置)
'''
def getSecond(*args):
	'''时间的秒数
	'''
	if args:
		args = list(args[:9])
		sub = 9 - len(args)
		if sub > 0:
			args.extend([0 for i in xrange(sub)])
		return int(time.mktime(args))
	
	ti = int(time.time())
	
	import timerEvent
	if timerEvent.gTempTime is not None:
		ti += timerEvent.gTempTime

	return ti

def getMinuteNo(i=0):
	'''分钟序号
	'''
	import timeU
	if not i:
		i = getSecond()
	return timeU.getMinuteNo(i)

def getHourNo(i=0):
	'''小时序号
	'''
	import timeU
	if not i:
		i = getSecond()
	return timeU.getHourNo(i)

def getDayNo(i=0):
	'''天序号
	'''
	import timeU
	if not i:
		i = getSecond()
	return timeU.getDayNo(i)

def getWeekNo(i=0):
	'''周序号
	'''
	import timeU
	if not i:
		i = getSecond()
	return timeU.getWeekNo(i)

def getMonthNo(i=0):
	'''月序号
	'''
	import timeU
	if not i:
		i = getSecond()
	return timeU.getMonthNo(i)

def getYearNo(i=0):
	'''年序号
	'''
	datePart = getDatePart()
	return datePart["year"]

def getDatePart(ti=0, partName=None):
	'''获取年、月、日等
	'''
	if not ti:
		ti = getSecond()
	tm = time.localtime(ti)

	datePart = {
		"year": tm.tm_year,
		"month": tm.tm_mon,
		"day": tm.tm_mday,
		"hour": tm.tm_hour,
		"minute": tm.tm_min,
		"second": tm.tm_sec,
		"wday": tm.tm_wday + 1,
	}
	
	if partName:
		return datePart[partName]
	return datePart
	
def formatDate(ti=0):
	'''格式化日期
	'''
	if not ti:
		ti = getSecond()
	tm = time.localtime(ti)
	return time.strftime("%Y年%m月%d日 %H时%M分%S秒", tm)

def formatTime(ti):
	'''格式化时间 
	'''
	if ti <= 0:
		return "0秒"

	day = ti / (3600 * 24)
	hour = ti % (3600 * 24) / 3600
	minute = ti % (3600 * 24) % 3600 / 60
	second = ti % (3600 * 24) % 3600 % 60
	
	txtList = []
	if day:
		txtList.append("%d天" % day)
	if hour:
		txtList.append("%d小时" % hour)
	if minute:
		txtList.append("%d分" % minute)
	if second:
		txtList.append("%d秒" % second)
	
	return "".join(txtList)

def writeLog(fileName, content):
	'''写日志
	'''
	import log
	log.log(fileName, content)
	
def calLen(s, encoding="utf-8"):
	'''计算字符串长度
	
	encoding: 字符串的编码
	'''
	return len(s.decode(encoding))

def calLenForWord(s, encoding="utf-8"):
	'''计算发言内容长度
	表情长度为2
	其他的计算其中的文本长度()
	'''
	s = re.sub("#.*?#n", _replaceFunc, s) # 链接(#L23#文本#颜色编号#n),有色文本(#C颜色编号内容文本#n)
	s = re.sub("#\d{1,3}", "**", s) # 表情(#1、#111)
	return calLen(s, encoding)

def _replaceFunc(m):
	s = m.group(0)
	m = re.match(".*\*(.*)\*.*", s)
	if m:
		s = m.group(1)
	return s

def logException():
	'''记录报错
	'''
	import misc
	misc.logException()
	
def getValByName(obj, attrName):
	'''根据属性名获取属性值
	'''
	#如:
	#teamId -> getTeamObj()
	#guildId -> getGuildObj()
	sOriAttrName=attrName
	if len(attrName)>=2 and attrName[0].islower() and attrName[1].isupper():#去掉proto msg 域上的类型前缀
		attrName=attrName[1:]

	if attrName.endswith("Id"):
		funcName = "get%sObj" % toTitle(attrName[:-2])
		func = getattr(obj, funcName, None)
		if func:
			attrObj = func()
			if attrObj:
				return attrObj.id
			return 0
	
	#如:
	#addon -> getAddon()
	#star -> getStar()
	#life -> getLife()
	func = getattr(obj, "get%s" % toTitle(attrName), None)
	if func:
		return func()
	
	#如:
	#carry -> isCarry()
	#fighter -> isFighter()
	func = getattr(obj, "is%s" % toTitle(attrName), None)
	if func:
		return func()
	
	#对象属性或属性方法
	for attrName in (sOriAttrName,toTitle(attrName),toNoTitle(attrName)):
		if hasattr(obj, attrName):
			val = getattr(obj, attrName)
			if callable(val):
				val = val()
			return val

	return obj.fetch(attrName)

def transCode(obj, code, *args):
	'''数值转化公共接口
	'''
	if isinstance(code, str): # 字符串，如:20*10+100,LV*20+100
		varNameList = re.findall("[a-zA-Z]+", code)
		if varNameList:
			varNameList = list(set(varNameList))
			varNameList.sort(reverse=True)
			params = {}
			for varName in varNameList:
				varVal = obj.getValueByVarName(varName, *args)
				code = code.replace(varName, str(varVal))
		return eval(code)
	if type(code) in (types.FunctionType, types.MethodType): # lambda函数，如:lambda LV:LV*20+100
		func = code
		params = []
		for varName in func.func_code.co_varnames:
			if varName == "self":
				continue
			varVal = obj.getValueByVarName(varName, *args)
			params.append(varVal)
		return func(*params)
	return code

def toTitle(s):
	'''转成标题格式(首字母大写)
	'''
	if not s:
		return s
	return s[0].upper() + s[1:]

def toNoTitle(s):
	'''转成小驼峰格式(首字母小写)
	'''
	if not s:
		return s
	return s[0].lower() + s[1:]

def formatToHTML(content):
	return '''<html>
<head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
</head>
<body>
%s
</body>''' % content

def isNumber(val):
	'''是否数字
	'''
	if re.match("^[+-]?\d+(\.\d+)?$", val):  # 整数或小数
		return 1
	return 0

def isInteger(val):
	'''是否整数
	'''
	if re.match("^[+-]?\d+$", val):  # 整数或小数
		return 1
	return 0

def isFloat(val):
	'''是否小数
	'''
	if re.match("^[+-]?\d+\.\d+$", val):  # 整数或小数
		return 1
	return 0

import time
import random
import re
import types
