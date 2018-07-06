#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def getChat(chatIdx):
	if chatIdx not in gdData:
		raise PlannerError,'不存在编号为{}的对白'.format(chatIdx)
	return gdData[chatIdx]

#导表开始
gdData={
	10001:'''错过的日常活动已转化为#C07{}点#C07历练经验#n，完成日常活动时，历练经验将会转化为人物经验''',
}
#导表结束