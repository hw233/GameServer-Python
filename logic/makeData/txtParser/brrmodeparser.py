#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#关卡模式表分析器
class cTxtParser(makeData.txtParser.cTxtParser):

	#override
	def getParseTxt(self):
		tFieldName=("PassExp","StdSec","StdPoint","StdDmg","TurnCard","InitPos")
		lKeyList1=[]
		lValList1=[]
		lKeyList2=[]
		lValList2=[]
		sKey0=""

		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeDict(tFieldName,lLine[2:],False)
			lKeyList2.append(lLine[1])
			lValList2.append(sTemp)

			if lLine[0]!="":
				sKey0=lLine[0]

			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeDict(lKeyList2,lValList2,True,2)
				lKeyList2=[]
				lValList2=[]
				lKeyList1.append(sKey0)
				lValList1.append(sTemp)

		return self.makeDict(lKeyList1,lValList1,True,1)



