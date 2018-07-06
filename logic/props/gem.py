#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):
	def __init__(self,iNo):
		props.object.cProps.__init__(self,iNo)
		
	@property
	def kind(self):
		return ITEM_GEM

	'''
	def getGemConfig(self,sKey,uDefault=0):
		return equipGem.getConfig(self.no(),sKey,uDefault)

	def _buttons(self):#override
		return [props_pb2.SELL]#,props_pb2.COMPOUND]

	def panel(self):
		return c.GEM_PANEL

	@property
	def level(self):
		return self.getGemConfig('lv')

	def type(self):
		return self.getGemConfig('gemType')

	def fightAbility(self):
		return getFightByGemNo(self.no())
	'''

	def maxStack(self):#override
		i=self.getConfig('叠加上限', sys.maxint)
		return i

	def getEffect(self):
		'''效果，把配表的原始数据生成处理一下，方便调用
		'''
		if not hasattr(self, "effect"):
			effect = {}
			for name, val in props.object.cProps.getEffect(self).iteritems():
				if name in descAttrList:
					name = descAttrList[name]
				effect[name] = val
			self.effect = effect
		return self.effect

def getBaseAttrByGemNo(iGemNo): 
		dBase={}
		for sKey,iType in c.ATTR_MAP4.iteritems():
			iValue=equipGem.getConfig(iGemNo,sKey)
			if not iValue:
				continue
			dBase[iType]=iValue
		return dBase

def compareGemByGemNo(iGemNo1,iGemNo2):#通过编号对比两个宝石,用于排序
	ilv1=equipGem.getConfig(iGemNo1,'lv')
	ilv2=equipGem.getConfig(iGemNo2,'lv')
	if ilv1==ilv2:
		iSortPos1=gdGemSort.get(equipGem.getConfig(iGemNo1,'gemType'))
		iSortPos2=gdGemSort.get(equipGem.getConfig(iGemNo2,'gemType'))
		if iSortPos1==iSortPos2:
			return 0
		return 1 if iSortPos1>iSortPos2 else -1
	return 1 if ilv1<ilv2 else -1

def compareGem(iGem1,iGem2):#对比两个宝石,用于排序
	return compareGemByGemNo(iGem1.no(),iGem2.no())

def getFightByGemNo(iGemNo):
	iFightAbility=0
	for sKey,iKey in c.ATTR_MAP4.iteritems():
		iValue=equipGem.getConfig(iGemNo,sKey)
		if iKey==c.ATT or iKey==c.HIT or iKey==c.DODGE:
			iFightAbility+=iValue/2
		elif iKey==c.DEF:
			iFightAbility+=iValue/4
		elif iKey==c.HP_MAX:
			iFightAbility+=iValue/25
	return iFightAbility

def getLastGem(iGemNo):#得到上一级的宝石编号,用于宝石合成
	iLv=equipGem.getConfig(iGemNo,'lv')
	if iLv==1:
		return 0
	iGemType=equipGem.getConfig(iGemNo,'gemType')
	for iTarGemNo in equipGem.gdGemByType.get(iGemType):
		if iLv-equipGem.getConfig(iTarGemNo,'lv')==1:
			return iTarGemNo
	return 0

def getNextGem(iGemNo):#得到下一级的宝石编号,宝石合成界面刷新要用
	iLv=equipGem.getConfig(iGemNo,'lv')
	iGemType=equipGem.getConfig(iGemNo,'gemType')
	for iTarGemNo in equipGem.gdGemByType.get(iGemType):
		if equipGem.getConfig(iTarGemNo,'lv')-iLv==1:
			return iTarGemNo
	return 0


import sys
from role.defines import *
from props.defines import *
import c
import props_pb2
import u

#宝石的排序映射,攻击>生命>防御>命中>闪避>法力
gdGemSort={1:1,7:2,2:3,4:4,5:5,8:6}