#-*-coding:utf-8-*-

def getCost(cnt):
	cnt = 5 if cnt >= 5 else cnt
	return gdData[cnt]["费用"]

#导表开始
gdData={
	1:{"费用":100000},
	2:{"费用":200000},
	3:{"费用":400000},
	4:{"费用":800000},
	5:{"费用":3200000},
}
#导表结束