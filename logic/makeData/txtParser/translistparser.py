#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#传送列表分析器
class cTxtParser(makeData.txtParser.cTxtParser):

	#override
	def getParseTxt(self):
		lKey=[]
		lVal=[]
		lTupleItem=[]
		sKey0=""
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeTuple(lLine[1:],False)
			lTupleItem.append(sTemp)

			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeTuple(lTupleItem,False)
				lTupleItem=[]
				lKey.append(sKey0)
				lVal.append(sTemp)

		return self.makeDict(lKey,lVal,True,1)