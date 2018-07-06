#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import os.path
import makeData.pyMaker
import makeData.txtParser
import makeData.txtParser.dialogparser
import makeData.txtParser.launchParser


#副本或关卡代码生成器
class cPyMaker(makeData.pyMaker.cPyMaker):
	def __init__(self,sNo):
		self.sNo=sNo
		self.lParsers=[]

		sSrcPath=Language("txt/副本关卡/%0$s/npc表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.CConfigParser("\tdNpc",sSrcPath,"Name","pos","Shape")
			self.addParser(ps)


		sSrcPath=Language("txt/副本关卡/%0$s/怪物表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.CConfigParser("\tdMonster",sSrcPath,"Name","pos","Shape","Lv","ps","ns","gg","wx","tp","sf","hp","mp","wg","wf","fg","ff")
			self.addParser(ps)

		sSrcPath=Language("txt/副本关卡/%0$s/机关表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.CConfigParser("\tdTrap",sSrcPath,"Name","pos","Shape","hp")
			self.addParser(ps)


		sSrcPath=Language("txt/副本关卡/%0$s/事件表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.CConfigParser("\tdEvent",sSrcPath,"Trigger","Answer","Success","Fail")
			self.addParser(ps)

		sSrcPath=Language("txt/副本关卡/%0$s/场景表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.CConfigParser("\tdScene",sSrcPath,"Name","resno")
			self.addParser(ps)

		sSrcPath=Language("txt/副本关卡/%0$s/奖励表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.launchParser.CRewardParser("\tdReward",sSrcPath)
			self.addParser(ps)

		sSrcPath=Language("txt/副本关卡/%0$s/对白表.txt",sNo)
		if os.path.exists(sSrcPath):
			ps=makeData.txtParser.dialogparser.CChatParser("\tdChat",sSrcPath)
			self.addParser(ps)

	#override
	def getParserGroup(self):
		return self.lParsers

	#override
	def getDstPath(self):
		return 'script/instance/it%s.py'%self.sNo
