#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

def getData(iNo, sKey="", uDefault=0):
	if iNo not in rideData:
		raise PlannerError,'没有编号为{}的坐骑'.format(iNo)
	if not sKey:
		return rideData[iNo]
	return rideData[iNo].get(sKey,uDefault)

def getBuyPointInfo(buyNo):
	if buyNo not in rideBuyPointData:
		raise PlannerError,'没有编号为{}的点数'.format(buyNo)
	return rideBuyPointData[buyNo].values()

def getConfig(sKey):
	if sKey not in rideConfig:
		raise PlannerError,'不存在编号为{}的坐骑配置'.format(sKey)
	return rideConfig[sKey]
	
#导表开始
rideData={
	6001:{"名称":"紫金葫芦","描述":"很强力的坐骑","头像":3004,"造型":"6001(0,1,0,1,1,0,0)","染色":"0,1,0,1,1,0,0","速度":100,"灵力":1,"下一只坐骑":6002,"孵化时间":12,"点数消耗":1},
	6002:{"名称":"乾坤飞剑","描述":"很强力的坐骑","头像":3004,"造型":"6002(0,1,0,1,1,0,0)","染色":"0,1,0,1,1,0,0","速度":100,"灵力":1,"下一只坐骑":6003,"孵化时间":12,"点数消耗":1},
	6003:{"名称":"炫彩莲荷","描述":"很强力的坐骑","头像":3004,"造型":"6003(0,1,0,1,1,0,0)","染色":"0,1,0,1,1,0,0","速度":100,"灵力":2,"下一只坐骑":0,"孵化时间":24,"点数消耗":2},
}

rideBuyPointData={
	1001:{"元宝":1440,"增加点数":1440},
	1002:{"元宝":9072,"增加点数":10080},
	1003:{"元宝":34560,"增加点数":43200},
	1004:{"元宝":181440,"增加点数":259200},
}

rideConfig={
	"开放等级":17,
	"加速孵化消耗":1,
	"首只孵化奖励":10000,
	"坐骑点扣除周期":60,
	"灵气获取周期":60,
	"骑乘点上限":550000,
}
#导表结束