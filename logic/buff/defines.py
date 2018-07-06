# -*- coding: utf-8 -*-

# buff类型位置
BUFF_TYPEPOS_BUFF = 1 # 增益
BUFF_TYPEPOS_DEBUFF = 2 # 减益
BUFF_TYPEPOS_SEAL = 3 # 封印
BUFF_TYPEPOS_SPECIAL = 4 # 特殊

# buff类型
BUFF_TYPE_BUFF = 10 # 增益
# BUFF_TYPE_CURE = 11 # 治疗
BUFF_TYPE_DEBUFF = 20 # 减益
BUFF_TYPE_SEAL = 30 # 封印
# BUFF_TYPE_POISON = 31 # 毒
BUFF_TYPE_SPECIAL = 40 # 特殊

buffTypeDesc = {
	"增益": "BUFF_TYPE_BUFF",
	"减益": "BUFF_TYPE_DEBUFF",
	"封印": "BUFF_TYPE_SEAL",
	"特殊": "BUFF_TYPE_SPECIAL",
}

def getBuffTypeDesc(name):
	if name not in buffTypeDesc:
		raise Exception("错误的buff类型名")
	return buffTypeDesc[name]


#===============================================================================
# 公式代码转换
#===============================================================================
def pattern1(w, *args):
	return w.level * float(args(0)) / float(args[1]) + float(args[2])

def pattern2(w, *args):
	return w.level * float(args(0)) + float(args(1))

def pattern3(w, *args):
	return w.level * float(args(0))


codePatternList = (
	("LV\*(\S+)/(\S+)\+(\S+)", pattern1), # LV*10/5+70
	("LV\*(\S+)\+(\S+)", pattern2), # LV*10+70
	("LV\*(\S+)", pattern3), # LV*10
)

def transCodeByPattern(pfObj, val, att=None, vic=None):
	'''根据正则表达式转换公式
	'''
	if isinstance(val, (int, float)):
		return int(val)
	if isinstance(val, str):
		if val.isdigit():
			return int(val)
		for pattern, func in codePatternList:
			m = re.match(pattern, val)
			if m:
				val = func(pfObj, att, vic, *m.groups())
				return int(val)
		
		return int(eval(val))
	
	return val

import re


