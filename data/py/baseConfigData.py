#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def getConfig(sKey):
	if sKey not in gdData:
		raise PlannerError("没有%s的配置数据" % sKey)
	return gdData[sKey]

#导表开始
gdData={
	"好友等级":10,
}
#导表结束