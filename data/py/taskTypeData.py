# -*- coding: utf-8 -*-

def getConfig(iNo, sKey, uDefault=0):
	if iNo not in gdData:
		raise PlannerError, '不存在编号为{}的任务类型'.format(iNo)
	return gdData[iNo].get(sKey, uDefault)

#导表开始
gdData={
	100:{"名称":"主线剧情"},
	200:{"名称":"常规任务"},
	300:{"名称":"红尘试炼"},
}
#导表结束

import u