#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇
#导表开始
gdData={
	1:(
		{"方案":1,"方案名称":"全力型","体质":0,"魔力":0,"力量":10,"耐力":0,"精神":0,"敏捷":0},
		{"方案":2,"方案名称":"均衡型","体质":2,"魔力":0,"力量":8,"耐力":0,"精神":0,"敏捷":0},
		{"方案":3,"方案名称":"敏捷型","体质":0,"魔力":0,"力量":8,"耐力":0,"精神":0,"敏捷":2},
	),
	2:(
		{"方案":1,"方案名称":"全法型","体质":0,"魔力":10,"力量":0,"耐力":0,"精神":0,"敏捷":0},
		{"方案":2,"方案名称":"均衡型","体质":2,"魔力":8,"力量":0,"耐力":0,"精神":0,"敏捷":0},
		{"方案":3,"方案名称":"敏捷型","体质":0,"魔力":8,"力量":0,"耐力":0,"精神":0,"敏捷":2},
	),
	3:(
		{"方案":1,"方案名称":"血牛型","体质":10,"魔力":0,"力量":0,"耐力":0,"精神":0,"敏捷":0},
		{"方案":2,"方案名称":"纯防型","体质":6,"魔力":0,"力量":0,"耐力":2,"精神":2,"敏捷":0},
		{"方案":3,"方案名称":"敏捷型","体质":8,"魔力":0,"力量":0,"耐力":0,"精神":0,"敏捷":2},
	),
}
#导表结束

def getPointInfo(iType, iScheme):
	data = gdData.get(iType,{})
	if not data:
		return {}
	for scheme in data:
		if scheme["方案"] == iScheme:
			return scheme
	return {}

def getDefaultPointInfo(iType):
	if iType not in gdData:
		return None
	info = getPointInfo(iType, 2)
	if not info:
		return None
	from role.defines import baseAttrList, attrDescList
	scheme = {}
	for attr in baseAttrList:
		sName = attrDescList[attr]
		scheme[attr] = info.get(sName, 0)
	return scheme
