# -*- coding: utf-8 -*-
import makeData.txtParser.configparser
import makeData.txtParser.multiparser
import makeData.txtParser.groupparser
import makeData.txtParser.chatparser
import makeData.pyMaker.taskmaker
import makeData.txtParser.kvParser

def make(ep, taskId):
	'''活动导表
	'''
	psList = []
	srcPath = "data/sl/task/t%05d/{}.sl" % taskId
	psList.append(makeData.txtParser.cTxtParser("main", srcPath.format("task")))
	psList.append(makeData.txtParser.configparser.cTxtParser("npcInfo", srcPath.format("npc"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("eventInfo", srcPath.format("event"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("rewardInfo", srcPath.format("reward"), ignore=True))
	psList.append(makeData.txtParser.multiparser.cTxtParser("rewardPropsInfo", srcPath.format("rewardprops"), ignore=True))
	psList.append(makeData.txtParser.groupparser.cTxtParser("groupInfo", srcPath.format("group"), ignore=True))
	psList.append(makeData.txtParser.chatparser.cTxtParser("chatInfo", srcPath.format("chat"), ignore=True))
	psList.append(makeData.txtParser.multiparser.cTxtParser("branchInfo", srcPath.format("branch"), ignore=True))
	psList.append(makeData.txtParser.multiparser.cTxtParser("fightInfo", srcPath.format("fight"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("ableInfo", srcPath.format("able"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("lineupInfo", srcPath.format("lineup"), ignore=True))
	psList.append(makeData.txtParser.kvParser.cTxtParser("configInfo", srcPath.format("config")))

	for info in parserList.get(taskId, []):
		mod = info["mod"]
		name = info["name"]
		fileName = info.get("file", name)
		psList.append(mod.cTxtParser(name, srcPath.format(fileName), ignore=True))
	
	maker = makeData.pyMaker.taskmaker.PyMaker(taskId, *psList)
	maker.makeToPyFile()
	ep.rpcTips("生成任务%d数据OK" % taskId)


# 额外的分析器
parserList = {
	10301:(
		{"mod":makeData.txtParser.configparser, "name":"monsterData"},
	),
	30001:(
		{"mod":makeData.txtParser.multiparser, "name":"ringTask"},
		{"mod":makeData.txtParser.multiparser, "name":"lastRingTask"},
		{"mod":makeData.txtParser.kvParser, "name":"schoolPoint"},
	),
	30101:(
		{"mod":makeData.txtParser.groupparser, "name":"nameInfo"},
		{"mod":makeData.txtParser.configparser, "name":"globalInfo"},
		{"mod":makeData.txtParser.configparser, "name":"mapInfo"},
	),
	30201:(
		{"mod":makeData.txtParser.multiparser, "name":"ringTask"},
		{"mod":makeData.txtParser.multiparser, "name":"lastRingTask"},
	),
	30601:(
		{"mod":makeData.txtParser.multiparser, "name":"ringTask"},
		{"mod":makeData.txtParser.multiparser, "name":"propsWeight"},
	),
	50001:(
		{"mod":makeData.txtParser.multiparser, "name":"groupTask"},
	),
	30501:(
		{"mod":makeData.txtParser.configparser, "name":"summonMonsterInfo", "file":"summonMonster"},
	),
	20301:(
		{"mod":makeData.txtParser.configparser, "name":"bossDescInfo", "file":"bossdesc"},
	),
}
	
