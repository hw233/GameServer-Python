# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	'''单项导表，如对白表
	'''

	def getParseTxt(self):
		lineList = self.parseTxtTo2dGroup()
		if not lineList:
			return "{\n}"

		titleList = lineList.pop(0)
		keyList = []
		valList = []
		tmpList = []
		lastKey = None
		for i, v in enumerate(lineList):
			if v[0]:
				lastKey = v[0]
			
			val = eval(v[1])
			val = val.replace("\n", "\\n")
			if tmpList:
				val = "\\nQ" + val
			tmpList.append(val)

			if self.isLastInGroup(lineList, i, 0):
				keyList.append(lastKey)

				val = "".join(tmpList)
				val = "'''%s'''" % val
				valList.append(val)
				tmpList = []
				lastKey = None
		
		return self.makeDict(keyList, valList, True, 1)







