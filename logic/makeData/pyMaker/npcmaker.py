#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import os.path
import makeData.pyMaker
import makeData.txtParser
import makeData.txtParser.dialogparser
import makeData.txtParser.launchParser


#npc代码生成器
class cPyMaker(makeData.pyMaker.cPyMaker):
	def __init__(self,sNpcNo):
		self.sNpcNo=sNpcNo
		self.lParsers=[]
#		sEventPath=Language("txt/npc/%s_事件表.txt")%sNpcNo
#		if os.path.exists(sEventPath):

#			self.lParsers.append(self.ep)
#
		sRewardPath=Language("txt/npc/%0$s_奖励表.txt",sNpcNo)
		if os.path.exists(sRewardPath):
			self.rp=makeData.txtParser.launchParser.CRewardParser("\tdReward",sRewardPath)
			self.addParser(self.rp)

		sChatPath=Language("txt/npc/%0$s_对白表.txt",sNpcNo)
		if os.path.exists(sChatPath):
			self.cp=makeData.txtParser.dialogparser.CChatParser("\tdChat",sChatPath)
			self.addParser(self.cp)

	#override
	def getParserGroup(self):
		return self.lParsers

	#override
	def getDstPath(self):
		return 'script/npc/n%s.py'%self.sNpcNo