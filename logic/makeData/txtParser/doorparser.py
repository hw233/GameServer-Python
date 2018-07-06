#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#传送点分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKey=[]
		lVal=[]
		lTupleItem=[]
		sKey0=""

		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			sPos=self.makeTuple(lLine[1:3],False)
			#sBarrier=lLine[3]
			sTarget=self.makeTuple(lLine[3:6],False)

			sAPort=self.makeDict(["Pos","Dst","Shape","Dir"],[sPos,sTarget,lLine[6],lLine[7]],False)
			lTupleItem.append(sAPort)
			if lLine[0]!="":
				sKey0=lLine[0]

			if self.isLastInGroup(lLines,iRow,0):
				lKey.append(sKey0)
				sTemp=self.makeTuple(lTupleItem,True,2)
				lVal.append(sTemp)
				lTupleItem=[]

		return self.makeDict(lKey,lVal,True,1)