# -*- coding: utf-8 -*-

# 基础属性
baseAttrList = (
	"con",
	"mag",
	"str",
	"res",
	"spi",
	"dex",
)

# 属性描述
attrDescList = {
	"con": "体质",
	"mag": "魔力",
	"str": "力量",
	"res": "耐力",
	"spi": "精神",
	"dex": "敏捷",
	
	"hp": "生命",
	"mp": "真气",
	"sp": "愤怒",
	"fuwen": "符能",
	"phyDam": "物理伤害",
	"magDam": "法术伤害",
	"phyDef": "物理防御",
	"magDef": "法术防御",
	"spe": "速度",
	"cure": "治疗强度",
	"phyCrit": "物理暴击",
	"magCrit": "法术暴击",
	"phyReCrit": "物理抗暴",
	"magReCrit": "法术抗暴",
	
	"phyRest": "物理抗性",
	"magRest": "法术抗性",

	"hpMax": "生命上限",
	"mpMax": "真气上限",
	
	"sealHit": "封印命中",
	"reSealHit": "抵抗封印",
}

# 描述对应的属性
descAttrList = {v:k for k,v in attrDescList.items()}


# 门派
schoolList = {
	11: "蜀山",
	12: "唐门",
	13: "武林盟",
	14: "苗疆",
	15: "魔宫",
	16: "佛门",
}

# 门派额外附加效果
schoolApply = {
	11: {"phyDam":2, "magDam":0, "phyDef":1, "magDef":0, "cure":0},
	12: {"phyDam":0, "magDam":2, "phyDef":0, "magDef":1, "cure":0},
	13: {"phyDam":2, "magDam":0, "phyDef":1, "magDef":0, "cure":0},
	14: {"phyDam":0, "magDam":2, "phyDef":0.5, "magDef":0.5, "cure":0},
	15: {"phyDam":0, "magDam":2, "phyDef":0, "magDef":1, "cure":0},
	16: {"phyDam":0, "magDam":0, "phyDef":0.5, "magDef":0.5, "cure":2}
}

# 性别
MALE = 1 # 男性
FEMALE = 2 # 女性

# 男性造型
maleList = {
	1111:"",
	1211:"",
	1311:"",
	1411:"",
	1511:"",
	1611:"",
}

# 女性造型
femaleList = {
	1121:"",
	1221:"",
	1321:"",
	1421:"",
	1521:"",
	1621:"",
}

# 实体附加状态
ADDON_TEAM_LEADER = 0x1  # 队伍的队长
ADDON_FIGHT = 0x2  # 战斗中
# ADDON_MAINTASK = 0x4  # 主线任务
# ADDON_FIGHTTASK = 0x8  # 战斗任务
ADDON_ESCORT = 0x10  # 运镖中
ADDON_TREASURE = 0x20  # 探宝中

shapePartTypeCount = 7 # 造型部位数

# 造型部位类型
SHAPE_PART_TYPE_HAIR = 0  # 头发
SHAPE_PART_TYPE_BODY = 1  # 身躯
SHAPE_PART_TYPE_CLOTHES = 2  # 衣服
SHAPE_PART_TYPE_WEAPON = 3  # 武器
SHAPE_PART_TYPE_SHADOW = 4  # 影子
SHAPE_PART_TYPE_HAT = 5  # 帽子
SHAPE_PART_TYPE_SHINE = 6  # 武器特效

# 造型部位类型描述
shapePartDesc = {
	SHAPE_PART_TYPE_HAIR: "头发",
	SHAPE_PART_TYPE_BODY: "身躯",
	SHAPE_PART_TYPE_CLOTHES: "衣服",
	SHAPE_PART_TYPE_WEAPON: "武器",
	SHAPE_PART_TYPE_SHADOW: "影子",
	SHAPE_PART_TYPE_HAT: "帽子",
	SHAPE_PART_TYPE_SHINE: "武器特效",

}


def getSchoolApply(sch, attr):
	'''获取门派额外附加效果
	'''
	if sch in schoolApply:
		return schoolApply[sch].get(attr, 0)
	return 0

def getAttrDesc(*attrList):
	lst = []
	for attr in attrList:
		lst.append(attrDescList[attr])
	
	if len(attrList) == 1:
		return lst[0]
		
	return lst

def randShapeParts(shapeId):
	'''随机套装
	'''
	shapeParts = {}
	for shapePartType in range(0, shapePartTypeCount):
		shapeParts[shapePartType] = shapePartScope.getShapePartByRand(shapeId, shapePartType)
	return shapeParts

def transToShapePartList(shapeParts):
	'''玩家造型部位转换成列表，用于发协议
	'''
	lst = []
	for shapePartType in range(0, shapePartTypeCount):
		if shapePartType in shapeParts:
			v = shapeParts[shapePartType]
		elif shapePartType < 5:
			v = 1
		else:
			v = 0
		lst.append(v)

	return lst

def transToShapePartListForPet(shapeParts):
	'''宠物造型部位转换成列表，用于发协议
	'''
	lst = []
	for shapePartType in range(0, shapePartTypeCount):
		if shapePartType in shapeParts:
			v = shapeParts[shapePartType]
		elif shapePartType == 1:
			v = 1
		else:
			v = 0
		lst.append(v)

	return lst

def transToShapePartListForRide(shapeParts):
	'''坐骑造型部位转换成列表，用于发协议
	'''
	lst = []
	for shapePartType in range(0, shapePartTypeCount):
		if shapePartType in shapeParts:
			v = shapeParts[shapePartType]
		elif shapePartType < 5:
			v = 1
		else:
			v = 0
		lst.append(v)

	return lst

def transToColorList(colors):
	'''玩家染色转换成列表，用于发协议(其实玩家染色用的是部位)
	'''
	lst = []
	for shapePartType in range(0, shapePartTypeCount):
		if shapePartType in colors:
			v = colors[shapePartType]
		else:
			v = 0
		lst.append(v)
	return lst

def transToColorListForPet(colors):
	'''宠物染色转换成列表，用于发协议
	'''
	lst = []
	for shapePartType in range(0, shapePartTypeCount):
		if shapePartType in colors:
			v = colors[shapePartType]
		else:
			v = 0
		lst.append(v)

	return lst
		
import shapePartScope

def transToColorListForRide(colors):
	'''坐骑染色转换成列表，用于发协议
	'''
	lst = []
	for shapePartType in range(0, shapePartTypeCount):
		if shapePartType in colors:
			v = colors[shapePartType]
		else:
			v = 0
		lst.append(v)

	return lst
		
import shapePartScope
