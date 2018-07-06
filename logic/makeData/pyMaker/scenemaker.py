#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import os.path
import makeData.pyMaker
import makeData.txtParser
import makeData.txtParser.stablenpcparser
import makeData.txtParser.stablemonsterparser
import makeData.txtParser.doorparser

class cPyMaker(makeData.pyMaker.cPyMaker):
	def __init__(self):
		self.lParsers=[]
		sSrcPath=Language("txt/场景/场景表.txt")
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.CConfigParser("gdScene",sSrcPath,"Name","Res","level")
			self.addParser(ps)

#		sSrcPath=Language("txt/场景/场景固定npc表.txt")
#		if os.path.exists(sSrcPath):
#			ps=makeData.txtParser.stablenpcparser.CStableNpcParser("gdStableNpc",sSrcPath)
#			self.lParsers.append(ps)

#		sSrcPath=Language("txt/场景/场景怪物表.txt")
#		if os.path.exists(sSrcPath):
#			ps=makeData.txtParser.stablemonsterparser.CStableMonsterParser("gdStableMonster",sSrcPath)
#			self.lParsers.append(ps)

#		sSrcPath=Language("txt/场景/传送点表.txt")
#		if os.path.exists(sSrcPath):
#			ps=makeData.txtParser.doorparser.CDoorParser("gdDoorInfo",sSrcPath)
#			self.lParsers.append(ps)


	#override
	def getParserGroup(self):
		return self.lParsers

	#override
	def getDstPath(self):
		return 'script/scene/SceneData.py'