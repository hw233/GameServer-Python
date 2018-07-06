# -*- coding: utf-8 -*-
'''key-value对
'''
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	
	def getParseTxt(self):
		dataList = self.parseTxtTo2dGroup()
		if not dataList:
			return "{\n}"

		txtList = []
		for line in dataList:
			k, v = line
			k = self.transVal(k)
			v = self.transVal(v)
			txtList.append("{}:{},".format(k, v))

		dataStr = "\n".join(txtList)
		return "{\n%s\n}" % indent(dataStr, 1)
	
	def transVal(self, val):
		val = val.strip("\"")
		if isNumber(val) or isList(val) or isTuple(val) or isDict(val):
			pass
		else:
			val = "\"{}\"".format(val)
		return val

from makeData.defines import *