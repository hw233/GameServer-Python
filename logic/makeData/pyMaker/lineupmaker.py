# -*- coding: utf-8 -*-
import makeData.pyMaker

class PyMaker(makeData.pyMaker.cPyMaker):
	
	def formatDataByTitle(self, parser, titleName, val, fmt):
		if titleName.startswith("位置"):
			applyStr = transApplyList(val, False, 0)
			return "{%s}" % applyStr
		return None
	
	
from makeData.defines import *
