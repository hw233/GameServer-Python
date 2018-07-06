#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#已经作废
#场景固定npc分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKey=[]
		lVal=[]
		lTupleItem=[]
		lLines=self.parseTxtTo2dGroup()
		sKey0=""
		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeTuple(lLine[1:],False)
			lTupleItem.append(sTemp)
			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				lKey.append(sKey0)
				sTemp=self.makeTuple(lTupleItem,True,2)
				lVal.append(sTemp)
				lTupleItem=[]

		return self.makeDict(lKey,lVal,True,1)