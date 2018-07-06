# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):

	def getParseTxt(self):
		dataList = self.parseTxtTo2dGroup()
		if not dataList:
			return "{\n}"

		lKey = []
		lValue = []
		lst = []
		iEnd = len(dataList)

		for iRow,lLine in enumerate(dataList):
			if iRow == 0:
				continue

			if lLine[2]:
				lKey.append(lLine[2])
				if iRow != 1:
					lValue.append(self.makeList(lst))
					lst = []

			lst.append(lLine[4])

			if iRow == iEnd - 1:
				lValue.append(self.makeList(lst))

		return self.makeDict(lKey,lValue,True)