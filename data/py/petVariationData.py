#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def getConfig(iNo, sKey="", uDefault=0):
	import u
	if iNo not in gdData:
		raise PlannerError,'没有编号{}的类型'.format(iNo)
	if not sKey:
		return gdData[iNo]
	return gdData[iNo].get(sKey,uDefault)

#导表开始
gdData={
	1:{"特长资质档次":5,"其余档次总和":18},
	2:{"特长资质档次":5,"其余档次总和":18},
	3:{"特长资质档次":5,"其余档次总和":18},
}
#导表结束