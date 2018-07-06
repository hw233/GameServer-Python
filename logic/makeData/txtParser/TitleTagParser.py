#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#称号标签表分析器
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
		tFieldName=("TagName","Name","Ratio")
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			if lLine[0]!="":				#每组第一行
				sKey0=lLine[0]
				lKeyList2.append(tFieldName[0])
				lValList2.append(lLine[1])
			lKeyList3.append(tFieldName[1])
			lValList3.append(lLine[3])
			lKeyList3.append(tFieldName[2])
			lValList3.append(lLine[4])
			sTemp3=self.makeDict(lKeyList3,lValList3,False,3)
			lKeyList2.append(lLine[2])
			lValList2.append(sTemp3)
			lKeyList3=[]
			lValList3=[]
			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeDict(lKeyList2,lValList2,True,2)
				lKeyList2=[]
				lValList2=[]
				lKeyList3=[]
				lValList3=[]
				lKeyList1.append(sKey0)
				lValList1.append(sTemp)

		return self.makeDict(lKeyList1,lValList1,True,1)

