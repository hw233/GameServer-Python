# -*- coding: utf-8 -*-
if "gModuleList" not in globals():
	gModuleList = {}
	
def hasModule(propsNo):
	return propsNo in gModuleList
	
def getModule(propsNo):
	if propsNo not in gModuleList:
		raise PlannerError("找不到编号为%d的物品" % propsNo)
	return gModuleList[propsNo]

def addModule(propsNo, mod):
	'''物品编号关联到模块
	'''
	global gModuleList
	gModuleList[propsNo] = mod
	
def initModule():
	'''初始化物品模块
	'''
	# 物品编号关联
	for propsNo, mod in propsNo2Module.iteritems():
		addModule(propsNo, mod)

	# 分类导表数据关联
	for dataMod, mod in data2Module.iteritems():
		for propsNo in dataMod.gdData.iterkeys():
			if hasModule(propsNo):
				continue
			addModule(propsNo, mod)
	
	# 通用导表数据关联，默认模块是 props.object
	for propsNo, data in propsData.gdData.iteritems():
		if hasModule(propsNo):
			continue
		propsType = data.get("类型", "")
		mod = type2Module.get(propsType, props.object)
		addModule(propsNo, mod)



#===============================================================================
# 分类导表数据关联到模块
# 用于大类物品
#===============================================================================
import propsData
import equipData
import props.equip
import levelmedicineData
import props.medicine.levelmedicine
import foodData
import props.food

data2Module = {
	equipData: props.equip,
	levelmedicineData: props.medicine.levelmedicine,
	foodData: props.food,
}


#===============================================================================
# 类型关联到模块
# 用于小类物品
#===============================================================================
import props.medicine.medicineRes
import props.medicine
import props.make
import props.lineupbook
import props.petskillbook
import props.gem
import props.giftBag
import props.giftGemBag
import props.experience
import props.virtual.eye
import props.eyeEffect
import props.heavyCast
import props.buddy

type2Module = {
	"储备药": props.medicine.medicineRes,
	"基础药": props.medicine,
	"制造符": props.make,
	"阵法书": props.lineupbook,
	"技能书": props.petskillbook,
	"宝石": props.gem,
	"礼包": props.giftBag,
	"宝石袋": props.giftGemBag,
	"经验丹": props.experience,
	"阵眼": props.virtual.eye,
	"兑换阵眼": props.eyeEffect,
	"重铸石": props.heavyCast,
	"伙伴" : props.buddy,
}


#===============================================================================
# 物品编号关联到模块
# 用于某个特殊处理的物品
#===============================================================================
import props.other.p202008
import props.other.p202006
import props.other.p202007
import props.other.p202040
import props.other.p202041
import props.other.p202047
import props.other.p202048
import props.other.p203001
import props.other.p203021
import props.other.p230011
import props.other.p230012
import props.other.p203014
import props.other.p203015
import props.other.p230021
import props.other.p203031
import props.other.p203032
import props.medicine.p221003
import props.medicine.p221301
import props.medicine.p221302
import props.food.p220001
import props.food.p220004
import props.food.p220007
import props.food.p220008
import props.food.p220009
import props.lineupbook.p224101
import props.virtual.p200001
import props.virtual.p200002
import props.virtual.p200003
import props.virtual.p200004
import props.virtual.p200005
import props.virtual.p200006
import props.virtual.p200007
import props.virtual.p200008
import props.virtual.p200009
import props.virtual.p200010
import props.virtual.p200011
import props.virtual.p200012
import props.virtual.p200051

propsNo2Module = {
	200001: props.virtual.p200001,
	200002: props.virtual.p200002,
	200003: props.virtual.p200003,
	200004: props.virtual.p200004,
	200005: props.virtual.p200005,
	200006: props.virtual.p200006,
	200007: props.virtual.p200007,
	200008: props.virtual.p200008,
	200009: props.virtual.p200009,
	200010: props.virtual.p200010,
	200011: props.virtual.p200011,
	200012: props.virtual.p200012,
	200051: props.virtual.p200051,
	202008: props.other.p202008,
	202006: props.other.p202006,
	202007: props.other.p202007,
	202040: props.other.p202040,
	202041: props.other.p202041,
	202047: props.other.p202047,
	202048: props.other.p202048,
	203001: props.other.p203001,
	203021: props.other.p203021,
	221003: props.medicine.p221003,
	221301: props.medicine.p221301,
	221302: props.medicine.p221302,
	220001: props.food.p220001,
	220004: props.food.p220004,
	220007: props.food.p220007,
	220008: props.food.p220008,
	220009: props.food.p220009,
	224101: props.lineupbook.p224101,
	230011: props.other.p230011,
	230012: props.other.p230012,
	203014: props.other.p203014,
	203015: props.other.p203015,
	230021: props.other.p230021,
	203031: props.other.p203031,
	203032: props.other.p203032,
}

