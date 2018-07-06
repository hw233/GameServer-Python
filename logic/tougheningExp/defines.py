# -*- coding: utf-8 -*-

MAX_GHOUGHENING_EXP = 500 * 10000	#历练经验上限


#由历练经验转化的人物经验的每日任务
RANGE = 1
SPECIFIC = 2
gdTransformDailyTask = {
	RANGE:[
		("task", 30100, 30199),	#降魔指引任务/降魔任务/离线降魔
		("task", 30000, 30099),	#师门指引任务/师门任务
		("task", 50200, 50250),	#秘册指引任务/秘册任务
		("task", 50251, 50300),	#月牙岛寻宝任务
		("task", 30201, 30300),	#帮会日常
		("task", 30301, 30400),	#运镖日常
		("task", 30401, 30499),	#竹林除妖
		("task", 30601, 30699),	#师门指引任务/师门任务
		("task", 30501, 30599),	#幻波池
		# ("task", 30200, 30299),	#仙盟任务
		("task", 20101, 20101),	#门派试炼
	],
	SPECIFIC:[
		"fengyao",		# 封妖 # 大衍藏宝秘册
		"answerDay",	# 每日答题
		"treasure",		# 幸运探宝
		"fairyland",	# 试炼幻境
		"race",			#单人竞技场
		"firstExam",	#天问初试
		"guildFight",	#仙盟大战
		"star",			#邪道煞星
		"teamRace",		#组队竞技场
		"triones",		#北斗七星
		"fiveBoss",		#五岳帝君
		"guildRobber",	#魔教入侵
		"schoolFight",	#门派试炼
		"guildMaze",	#仙盟迷宫
	],
	
}


def initTransformRange():
	'''初始化转化经验范围
	'''
	global glTransformRange
	glTransformRange = []

	for iType,lInfo in gdTransformDailyTask.iteritems():
		if iType == RANGE:
			for sType,iStart,iEnd in lInfo:
				for _iNo in xrange(iStart, iEnd+1):
					glTransformRange.append("{}{}".format(sType, _iNo))

		elif iType == SPECIFIC:
			glTransformRange.extend(lInfo)
		# else:
		# 	raise Exception,"历练经验转化的人物经验的每日任务类型不存在"

def isInTransformRange(sReason):
	'''是否为转化的人物经验的每日任务
	'''
	return sReason in glTransformRange


if "gbOnce" not in globals():
	gbOnce=True
	glTransformRange = {}
# 	if 'mainService' in SYS_ARGV:
# 		initTransformRange()





