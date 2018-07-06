# -*- coding: utf-8 -*-
import makeData.txtParser.configparser
import makeData.txtParser.multiparser
import makeData.txtParser.groupparser
import makeData.txtParser.chatparser
import makeData.pyMaker.collectMaker

def make(ep):
	'''活动导表
	'''
	psList = []
	srcPath = "data/sl/collect/{}.sl" 
	psList.append(makeData.txtParser.configparser.cTxtParser("eventInfo", srcPath.format("event"), ignore=True))
	psList.append(makeData.txtParser.multiparser.cTxtParser("fightInfo", srcPath.format("fight"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("ableInfo", srcPath.format("able"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("rewardInfo", srcPath.format("reward"), ignore=True))
	psList.append(makeData.txtParser.multiparser.cTxtParser("rewardPropsInfo", srcPath.format("rewardprops"), ignore=True))
	
	maker = makeData.pyMaker.collectMaker.PyMaker(*psList)
	maker.makeToPyFile()
	ep.rpcTips("生成室外收集数据OK")

