#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import multiField
#一个属性占一列的角色数据(方便统计与查询)
#每一个列独立出来都应该有充足的理由

#pro,lv gold为了统计方便需要独立一列
#name 创建角色时判断角色名是否被占用,需要独立一列

class cMultiField1(multiField.cMultiField):
	def __init__(self,iRoleId):#override
		self.iRoleId=iRoleId
		self.tWatchNames='sName','iExp','iLv','iPro','iWeapShape','iGold','iStatus','iArenaPoint','iVoucher'

		multiField.cMultiField.__init__(self,'多列数据块1',iRoleId)
		self.setIsStm(sql.ROLE_MULTI_FIELD1_INSERT)
		self.setDlStm(sql.ROLE_MULTI_FIELD1_DELETE)
		self.setUdStm(sql.ROLE_MULTI_FIELD1_UPDATE)
		self.setSlStm(sql.ROLE_MULTI_FIELD1_SELECT)
		#需要被存盘的成员变量初始值全部设为None,因为父类检查数据是否发生变化是依赖于发生变化的变量原来的值是否是None
		self.sName=self.iExp=self.iLv=self.iPro=self.wp=None
		self.iGold=self.iStatus=self.iLeagueRank=self.iArenaPoint=self.iVoucher=None

	def _getWatchNames(self):#override
		return self.tWatchNames

	def _dirtyEventHandler(self):#override
		factoryConcrete.multiField1Ftr.schedule2tail4save(self.iRoleId)

	def _getValuesTuple4Update(self):#override
		return self.iExp,self.iLv,self.iPro,self.iWeapShape,self.iGold,self.iArenaPoint,self.iVoucher

	def _getSelectRecordsetFieldCount(self):
		return 10

	def _setValuesAfterSelect(self,*tValues):#override
		self.sName,self.iExp,self.iLv,self.iPro,self.iWeapShape,self.iGold,self.iStatus,self.iLeagueRank,self.iArenaPoint,self.iVoucher=tValues
		# if not self.sName:
		# 	self.sName=c.BORN_NAME #原属性为None,不会触发观察列表值变化引起的存盘

	def _setSelectNoRecordsetDefaultValues(self,*itNoRowInsertValues):#override
		self.sName,self.iExp,self.iLv,self.iPro,self.iWeapShape,self.iGold,self.iStatus,self.iLeagueRank,self.iArenaPoint,self.iVoucher=itNoRowInsertValues[4:]
		# self.sName=c.BORN_NAME #原属性为None,不会触发观察列表值变化引起的存盘



import factoryConcrete
import misc
import config
import jitKeeper

#用于查看离线玩家的多列信息.一段时间后不访问,自动从容器上移除
if 'gKeeper' not in globals():
	KEEP_SECOND=30 if config.IS_INNER_SERVER else 60*5
	gKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.multiField1Ftr)

import role
import sql
import factoryConcrete
import c
