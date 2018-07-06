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
		lKeyList4=[]
		lValList4=[]
		sKey0=""
		tFieldName=("NAME","CONF","MD5","KEY")
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			lKeyList4.append(tFieldName[2])
			lValList4.append(lLine[3])
			lKeyList4.append(tFieldName[3])
			lValList4.append(lLine[4])
			sTemp4=self.makeDict(lKeyList4,lValList4,False,5)
			lKeyList4=[]
			lValList4=[]
			lKeyList3.append(lLine[2])
			lValList3.append(sTemp4)
			sTemp3=self.makeDict(lKeyList3,lValList3,True,4)
			if lLine[0]!="":				#每组第一行
				sKey0=lLine[0]
				lKeyList2.append(tFieldName[0])
				lValList2.append(lLine[1])


			if self.isLastInGroup(lLines,iRow,0):
				if sTemp3:
					lValList2.append(sTemp3)
					lKeyList2.append(tFieldName[1])

				sTemp=self.makeDict(lKeyList2,lValList2,True,2)
				lKeyList2=[]
				lValList2=[]
				lKeyList3=[]
				lValList3=[]
				lKeyList1.append(sKey0)
				lValList1.append(sTemp)

		return self.makeDict(lKeyList1,lValList1,True,1)


