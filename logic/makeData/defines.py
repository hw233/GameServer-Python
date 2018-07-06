# -*- coding: utf-8 -*-
from c import LINE_SEP

def transApplyList(applyListStr, isLine=True, indentN=1):
	'''转换效果
	'''
	if not applyListStr:
		return ""

	lst = []
	for applyStr in applyListStr.split("|"):
		m = re.match("([^:,]+)\:(.*)", applyStr)
		if m:
			applyName = m.group(1)
			applyVal = m.group(2)
			applyName, applyVal = formatApply(applyName, applyVal)
		else:
			applyName = applyStr
			applyVal = "True"
		lst.append("\"%s\":%s," % (applyName, applyVal))

	if isLine: # 换行
		applyListStr = LINE_SEP.join(lst)
	else:
		applyListStr = "".join(lst)
	
	if indentN: # 缩进
		return indent(applyListStr, indentN)
	return applyListStr

def formatApply(applyName, applyVal):
	if applyVal.endswith("%"):
		applyName += "加成"
		applyVal = applyVal[:-1]

	if isLambda(applyVal):
		applyVal = transLambda(applyVal)
	elif isList(applyVal) or isTuple(applyVal) or isNumber(applyVal) or isDict(applyVal):
		pass
	else:
		applyVal = "\"%s\"" % applyVal
		
	return applyName, applyVal

def transLambda(s, isInstancemethod=False):
	'''转成lambda表达式
	'''
	if not s:
		return ""
	params = re.findall("[a-zA-Z]+", s)
	if not params:
		return s
	params = set(params)
	params = ",".join(params)
	
	if isInstancemethod:
		return "lambda self,{}:{}".format(params, s)
	return "lambda {}:{}".format(params, s)

def isLambda(val):
	'''是否lambda表达式
	'''
	if re.search("[a-zA-Z]+", val):
		return True
	return False

def isNumber(val):
	'''是否数字
	'''
	if re.match("^[+-]?\d+(\.\d+)?$", val):  # 整数或小数
		return True
	return False

def isList(val):
	'''是否列表
	'''
	if re.match("^\[([^,\[\]]+,?)*\]$", val):
		return 1
	if re.match("^[^,\[\(\)]+,([^,\]\(\)]+,?)*$", val):  # 不带括号
		return 2
	return 0

def isTuple(val):
	'''是否元组
	'''
	if re.match("^\(([^,\(\)]+,?)*\)$", val):
		return 1
	if re.match("^[^,\(]+,([^,\)]+,?)*$", val):  # 不带括号
		return 2
	return 0

def isDict(val):
	'''是否字典
	'''
	if re.match("^\{([^,]+:[^,]+,?)*\}$", val):
		return 1
	if re.match("^([^,\{]+:[^,\}]+,?)*$", val):  # 不带括号
		return 2
	return 0

def indent(content, n=1, firstLine=True):
	'''缩进
	firstList: 第一行是否也缩进
	'''
	lst = []
	tab = "\t" * n
	for i, line in enumerate(content.split("\n")):
		if line.strip():
			if i != 0 or firstLine:
				line = tab + line
		lst.append(line)

	return "\n".join(lst)

def isValidStr(s):
	'''是否有效字符串
	'''
	if s in (None, "0", ""):
		return False
	return True

if __name__ == "__main__":
	import re
	applyStr = "伤害率:{0:55,1:60}|生命值限制:70|封印"
	print transApplyList(applyStr)


from common import *
import re
