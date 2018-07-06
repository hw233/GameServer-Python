#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
def getConfig(iNo, sKey="", uDefault=0):
	import u
	if iNo not in gdData:
		raise PlannerError,'没有编号为{}的宠物兑换'.format(iNo)
	if not sKey:
		return gdData[iNo]
	return gdData[iNo].get(sKey,uDefault)
#导表开始
gdData={
	2001:{"物品编号":230201,"消耗":50},
	2002:{"物品编号":230201,"消耗":50},
}
#导表结束