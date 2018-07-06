#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#辅助合区表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKeyList1=[]
		lValList1=[]
		lKeyList2=[]
		lValList2=[]
		lKeyList3=[]
		lValList3=[]
		sKey0=""
		tFieldName=("IsLastRef","PassTime","NeedGoods","KillMst","RepMstList")
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			sValTuple=self.makeTuple(lLine[3:],False,2)
			lValList3.append(sValTuple)
			sKeyTuple=self.makeTuple(lLine[1:3],False,2)
			lKeyList3.append(sKeyTuple)
			sTemp=self.makeDict(lKeyList3,lValList3,True,3)

			if lLine[0]!="":
				sKey0=lLine[0]

			if self.isLastInGroup(lLines,iRow,0):
				lKeyList1.append(sKey0)
				lValList1.append(sTemp)
				lKeyList3=[]
				lValList3=[]
		return self.makeDict(lKeyList1,lValList1,True,1)







