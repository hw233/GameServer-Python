#-*-coding:utf-8-*-
def getPos(school):
	if school not in gdData:
		raise '没有编号为{}的门派出生点'.format(school)
	return gdData[school]["坐标"]
#导表开始
gdData={
	11:{"坐标":(1070,13,41,8)},
	12:{"坐标":(1040,54,6,2)},
	13:{"坐标":(1030,72,49,8)},
	14:{"坐标":(1060,55,41,8)},
	15:{"坐标":(2040,90,64,8)},
	16:{"坐标":(2030,60,96,3)},
}
#导表结束