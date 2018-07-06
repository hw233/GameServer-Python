# -*- coding: utf-8 -*-

#===============================================================================
# 法术类型
#===============================================================================
PERFORM_TYPE_NONE = 0  # 无
PERFORM_TYPE_MAG = 1  # 魔法攻击
PERFORM_TYPE_PHY = 20  # 物理近攻
PERFORM_TYPE_PHY_REMOTE = 21  # 物理远攻
PERFORM_TYPE_CURE = 3  # 治疗
PERFORM_TYPE_BUFF = 40  # 增益
PERFORM_TYPE_BUFF_MP = 41  # 增益真气
PERFORM_TYPE_DEBUFF = 5  # 减益
PERFORM_TYPE_REVIVE = 6  # 复活
PERFORM_TYPE_SEAL = 7  # 封印
PERFORM_TYPE_RESEAL = 8 # 解封

performTypeNameDesc = {
	"无": "Perform",
    "魔法攻击": "MagAttackPerform",
    "物理近攻": "PhyAttackPerform",
    "物理远攻": "RemotePhyAttackPerform",
    "治疗": "CurePerform",
    "增益": "BuffPerform",
    "增益真气": "MPBuffPerform",
    "减益": "DeBuffPerform",
    "复活": "RevivePerform",
    "封印": "SealPerform",
    "解封": "ReSealPerform",
}


#===============================================================================
# 目标类型
#===============================================================================
PERFORM_TARGET_NONE = 0  # 无
PERFORM_TARGET_ENEMY = 1  # 敌方
PERFORM_TARGET_FRIEND = 2  # 己方
PERFORM_TARGET_SELF = 3  # 自己
PERFORM_TARGET_ANY = 4  # 任意

targetTypeNameDesc = {
	"无": "PERFORM_TARGET_NONE",
	"敌方": "PERFORM_TARGET_ENEMY",
	"己方": "PERFORM_TARGET_FRIEND",
	"自己": "PERFORM_TARGET_SELF",
	"任意": "PERFORM_TARGET_ANY",
}


#===============================================================================
# 五行
#===============================================================================
FIVE_EL_NONE = 0 # 没有五行属性
FIVE_EL_METAL = 1  # 金
FIVE_EL_WOOD = 2  # 木
FIVE_EL_WATER = 3  # 水
FIVE_EL_FIRE = 4 # 火
FIVE_EL_EARTH = 5  # 土
FIVE_EL_NOT = 6 # 无

fiveElDesc2Val = {
	"金": FIVE_EL_METAL,
	"木": FIVE_EL_WOOD,
	"水": FIVE_EL_WATER,
	"火": FIVE_EL_FIRE,
	"土": FIVE_EL_EARTH,
	"无": FIVE_EL_NOT,
}

fiveElVal2Desc = {v:k for k,v in fiveElDesc2Val.iteritems()}

fiveElDesc2ValStr = {
	"金": "FIVE_EL_METAL",
	"木": "FIVE_EL_WOOD",
	"水": "FIVE_EL_WATER",
	"火": "FIVE_EL_FIRE",
	"土": "FIVE_EL_EARTH",
	"无": "FIVE_EL_NOT",
}

def getFiveElVal(desc):
	'''获取五行值
	'''
	return fiveElDesc2Val.get(desc, 0)

def getFiveElDesc(val):
	'''获取五行描述
	'''
	return fiveElVal2Desc.get(val, "")


# 消耗或恢复处理列表
addHandleList = {
    "真气": {"属性名":"mp", "方法名":"addMP"},
    "生命": {"属性名":"hp", "方法名":"addHP"},
    "愤怒": {"属性名":"sp", "方法名":"addSP"},
    "符能": {"属性名":"fuwen", "方法名":"addFuWen"},
}

def doConsume(w, consumeName, consumeVal):
	'''消耗
	'''
	methodName = addHandleList[consumeName]["方法名"]
	func = getattr(w, methodName)
	func(-consumeVal)

#===============================================================================
# 公式代码转换
#===============================================================================
def pattern1(pfObj, att, vic, *args):
	return pfObj.getLevel(att) * float(args[0]) / float(args[1]) + float(args[2])

def pattern2(pfObj, att, vic, *args):
	return pfObj.getLevel(att) / float(args[0]) + float(args[1])

def pattern3(pfObj, att, vic, *args):
	return pfObj.getLevel(att) * float(args[0]) + float(args[1])

def pattern4(pfObj, att, vic, *args):
	return pfObj.getLevel(att) * float(args[0])

def pattern5(pfObj, att, vic, *args):
	return (pfObj.getLevel(att) - att.level + float(args[0])) / float(args[1]) + float(args[2])

def pattern6(pfObj, att, vic, *args):
	return att.level * float(args[0]) / float(args[1]) + float(args[2])

def pattern7(pfObj, att, vic, *args):
	return att.level / float(args[0]) + float(args[1])

def pattern8(pfObj, att, vic, *args):
	return att.level * float(args[0]) + float(args[1])

def pattern9(pfObj, att, vic, *args):
	return att.level * float(args[0])

def pattern10(pfObj, att, vic, *args):
	return (pfObj.getLevel(att) - att.level) * float(args[0]) + float(args[1])

def pattern11(pfObj, att, vic, *args):
	return -(float(args[0]) * pfObj.getLevel(att))

def pattern12(pfObj, att, vic, *args):
	return (pfObj.getLevel(att) - vic.level) * float(args[0]) + float(args[1])

def pattern13(pfObj, att, vic, *args):
	return (pfObj.getLevel(att) - vic.level + float(args[0])) / float(args[1]) + float(args[2])


codePatternList = (
	("^SLV\*(\S+)/(\S+)\+(\S+)$", pattern1), # SLV*10/5+70
	("^SLV/(\S+)\+(\S+)$", pattern2), # SLV/10+70
	("^SLV\*(\S+)\+(\S+)$", pattern3), # SLV*10+70
	("^SLV\*(\S+)$", pattern4), # SLV*10
	("^(\S+)\*SLV$", pattern4), # 2*SLV
	("^-\((\S+)\*SLV\)$", pattern11), # -(2*SLV)
	("^\(SLV\-LV\+(\S+)\)/(\S+)\+(\S+)$", pattern5), # (SLV-LV+10)/10+70
	("^\(SLV\-VLV\+(\S+)\)/(\S+)\+(\S+)$", pattern13), # (SLV-VLV+10)/10+70
	("^\(SLV-LV\)\*(\S+)\+(\S+)$", pattern10), # (SLV-LV)*2+70
	("^\(SLV-VLV\)\*(\S+)\+(\S+)$", pattern12), # (SLV-VLV)*2+70
	("^LV\*(\S+)/(\S+)\+(\S+)$", pattern6), # LV*5/10+70
	("^LV/(\S+)\+(\S+)$", pattern7), # LV/10+70
	("^LV\*(\S+)\+(\S+)$", pattern8), # LV*10+70
	("^LV\*(\S+)$", pattern9), # LV*10
	("^(\S+)\*LV$", pattern9), # 10*LV
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

def getValueByVarName(varName, att=None, vic=None):
	if varName == "LV":
		return att.level
	if varName == "VLV":
		return vic.level
	if varName == "HPR":
		return att.hp * 100 /att.hpMax
	if varName == "HPRV":
		return vic.hp * 100 /vic.hpMax
	if varName == "RND":
		return rand
	
	# 属性
	isAttr = False
	w = att
	if varName in role.defines.attrDescList:
		isAttr = True
	elif varName.endswith("V") and varName[:-1] in role.defines.attrDescList:
		isAttr = True
		w = vic
		varName = varName[:-1]
		
	if isAttr:
		if varName == "phyDam":
			return w.getPhyDamAll()
		if varName == "magDam":
			return w.getMagDamAll()
		if varName == "phyDef":
			return w.getPhyDefAll()
		if varName == "magDef":
			return w.getMagDefAll()
		if varName == "spe":
			return w.getSpeAll()
		return getattr(w, varName, 0)
	
	raise Exception("策划填的变量{}无法解析".format(varName))

from common import *
import role.defines
