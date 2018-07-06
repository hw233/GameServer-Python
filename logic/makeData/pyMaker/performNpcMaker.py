# -*- coding: utf-8 -*-
import makeData.pyMaker.performSchMaker

class PyMaker(makeData.pyMaker.performSchMaker.PyMaker):
	
	def getName(self):
		return "npc法术"

	def getMainModName(self, idx):
		return "perform.npcs.pf%s" % self.transIdx(idx)
