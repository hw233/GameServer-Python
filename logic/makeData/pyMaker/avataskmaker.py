#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import os.path
import makeData.pyMaker
import makeData.txtParser
import makeData.txtParser.dialogparser
import makeData.txtParser.launchParser

#可接任务表生成器
class cPyMaker(makeData.pyMaker.cPyMaker):
	def __init__(self):
		self.lParsers=[]
		sTaskPath=Language("Data/Uenc/可接任务.uenc")
		if os.path.exists(sTaskPath):
			self.tp=makeData.txtParser.CConfigParser("gdData",sTaskPath,"PanelNo","Name","Desc","issuer","Remote","FirstRing","issuechat","DayTimes","WeekTimes","MinLv","MaxLv")
			self.addParser(self.tp)

	#override
	def getParserGroup(self):
		return self.lParsers

	#override
	def getDstPath(self):
		return 'script/task/avatask.py'