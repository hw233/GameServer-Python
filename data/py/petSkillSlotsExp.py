#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def getExp(slot):
	return gdData.get(slot, {}).get("开启经验", -1)

#导表开始
gdData={
	1:{"开启经验":600},
	2:{"开启经验":1250},
	3:{"开启经验":2500},
	4:{"开启经验":5000},
	5:{"开启经验":8500},
	6:{"开启经验":15300},
	7:{"开启经验":27540},
	8:{"开启经验":49572},
	9:{"开启经验":74358},
	10:{"开启经验":111537},
	11:{"开启经验":167306},
	12:{"开启经验":250958},
}
#导表结束