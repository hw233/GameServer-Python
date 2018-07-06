#-*-coding:utf-8-*-

#导表开始
gdGuildMember={
	0:{"成员上限":50,"学徒上限":30},
	1:{"成员上限":75,"学徒上限":40},
	2:{"成员上限":100,"学徒上限":50},
	3:{"成员上限":125,"学徒上限":60},
	4:{"成员上限":150,"学徒上限":70},
	5:{"成员上限":175,"学徒上限":80},
}

gdGuildMaintain={
	1:{"资金":1125000},
	2:{"资金":1500000},
	3:{"资金":1875000},
	4:{"资金":2250000},
	5:{"资金":2625000},
}

gdGuildUpgrade={
	1:{"资金":3000000,"时间":1},
	2:{"资金":6000000,"时间":2},
	3:{"资金":12000000,"时间":4},
	4:{"资金":24000000,"时间":8},
	5:{"资金":48000000,"时间":16},
}

gdGuildWeight={
	1:{"权重":5},
	2:{"权重":4},
	3:{"权重":3},
	4:{"权重":2},
	5:{"权重":1},
}

gdGuildDepot={
	0:{"库房上限":15000000,"获得资金":2400000},
	1:{"库房上限":30000000,"获得资金":3600000},
	2:{"库房上限":45000000,"获得资金":4800000},
	3:{"库房上限":60000000,"获得资金":6000000},
	4:{"库房上限":75000000,"获得资金":7200000},
	5:{"库房上限":90000000,"获得资金":8400000},
}

gdGuildDoor={
	101:{"造型":1001,"场景编号":"$scene1","传送点x":71,"传送点y":36,"感应点":(70,35,),"目标场景编号":"$scene2","目标x":21,"目标y":13,"面向":1,"目标场景名称":"仙盟大厅"},
	102:{"造型":1001,"场景编号":"$scene2","传送点x":16,"传送点y":5,"感应点":(20,9,),"目标场景编号":"$scene1","目标x":68,"目标y":33,"面向":1,"目标场景名称":"仙盟大院"},
}
#导表结束

def getGuildMemberMax(guildLv, key):
	'''获取帮派成员上限
	'''
	if guildLv in gdGuildMember:
		return gdGuildMember[guildLv].get(key, 0)
	return 0

def getGuildMaintain(guildLv, key):
	'''获取帮派维护信息
	'''
	if guildLv in gdGuildMaintain:
		return gdGuildMaintain[guildLv].get(key, 0)
	return 0

def getBuildingUpgrade(idx, key):
	'''帮派建筑升级信息
	'''
	if idx in gdGuildUpgrade:
		return gdGuildUpgrade[idx].get(key, -1)
	return -2

def getWeight(job, key="权重"):
	return gdGuildWeight.get(job, {}).get(key, 0)
