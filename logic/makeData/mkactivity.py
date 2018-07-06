# -*- coding: utf-8 -*-
import makeData.txtParser.configparser
import makeData.txtParser.multiparser
import makeData.txtParser.groupparser
import makeData.txtParser.chatparser
import makeData.pyMaker.activitymaker
import makeData.txtParser.kvParser

def make(ep, activityName):
	'''活动导表
	'''
	psList = []
	srcPath = "data/sl/activity/%s/{}.sl" % activityName
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
	psList.append(makeData.txtParser.configparser.cTxtParser("sceneInfo", srcPath.format("scene"), ignore=True))
	psList.append(makeData.txtParser.kvParser.cTxtParser("configInfo", srcPath.format("config"), ignore=True))
	
	for info in parserList.get(activityName, []):
		mod = info["mod"]
		name = info["name"]
		fileName = info.get("file", name)
		psList.append(mod.cTxtParser(name, srcPath.format(fileName), ignore=True))
	
	maker = makeData.pyMaker.activitymaker.PyMaker(activityName, *psList)
	maker.makeToPyFile()
	ep.rpcTips("生成活动%s数据OK" % activityName)


# 额外的分析器
parserList = {
	"fengyao":(
		{"mod":makeData.txtParser.configparser, "name":"monsterData"},
		{"mod":makeData.txtParser.configparser, "name":"monsterConfig"},
		{"mod":makeData.txtParser.multiparser, "name":"propsEventRatio"},
		{"mod":makeData.txtParser.configparser, "name":"mapInfo"},

	),
	"center":(
		{"mod":makeData.txtParser.configparser, "name":"activityData"},
		{"mod":makeData.txtParser.configparser, "name":"rewardData"},
		{"mod":makeData.txtParser.configparser, "name":"jumpData"},
	),
	"treasure":(
		{"mod":makeData.txtParser.configparser, "name":"eventPoint"},
	),
	"guildRobber":(
		{"mod":makeData.txtParser.configparser, "name":"batchInfo"},
	),
	"instance":(
		{"mod":makeData.txtParser.configparser, "name":"instanceData"},
	),
	"fairyland":(
		{"mod":makeData.txtParser.configparser, "name":"stageData"},
		{"mod":makeData.txtParser.multiparser, "name":"rankReward"},
	),
	"star":(
		{"mod":makeData.txtParser.configparser, "name":"monsterData"},
		{"mod":makeData.txtParser.configparser, "name":"monsterConfig"},
	),
	"fiveBoss":(
		{"mod":makeData.txtParser.configparser, "name":"starchat"},
	),
	"triones":(
		{"mod":makeData.txtParser.configparser, "name":"monsterFactor"},
	),
}
	
