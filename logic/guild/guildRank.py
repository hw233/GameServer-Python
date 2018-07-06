#-*- coding:UTF-8 -*-
import pst

class cRank(pst.cEasyPersist):
	def __init__(self):
		pst.cEasyPersist.__init__(self)
		self.lRanking=[]
		self.dMaxContribution={}	#{iRoleId:iMaxContribution} 成员历史最高捐献

	def save(self):
		dData=pst.cEasyPersist.save(self)
		if self.lRanking:
			dData['r']=self.lRanking
		if self.dMaxContribution:
			dData['maxCtb']=self.dMaxContribution
		return dData

	def load(self,dData):
		pst.cEasyPersist.load(self,dData)
		self.lRanking=dData.pop('r',[])
		self.dMaxContribution=dData.pop('maxCtb',{})

	def update(self,iRoleId):
		iIdx1=findSort.binarySearchLeft(self.lRanking,iRoleId)
		iIdx2=findSort.binarySearchRight(self.lRanking,iRoleId)
		if iIdx1==iIdx2:
			print '{} not exists'.format(iRoleId)
			return
		self.lRanking.remove(iRoleId)
		findSort.binaryInsertRight(self.lRanking,iRoleId,self.dataComparer)

	def dataComparer(self,iRoleId1,iRoleId2):#比较器
		iContribution1=self.dMaxContribution.get(iRoleId1,0)
		iContribution2=self.dMaxContribution.get(iRoleId2,0)
		if iContribution1==iContribution2:
			return 0
		return 1 if iContribution1<iContribution2 else -1 #从大到小

	def addRecord(self,iRoleId):
		self.dMaxContribution[iRoleId]=0
		findSort.binaryInsertRight(self.lRanking,iRoleId,self.dataComparer)

	def removeRecord(self,iRoleId):
		self.dMaxContribution.pop(iRoleId,None)
		iIdx1=findSort.binarySearchLeft(self.lRanking,iRoleId)
		iIdx2=findSort.binarySearchRight(self.lRanking,iRoleId)
		if iIdx1==iIdx2:
			print '{} not exists'.format(iRoleId)
			return
		self.lRanking.remove(iRoleId)

	def getRoleRank(self,iRoleId):
		iIdx1=findSort.binarySearchLeft(self.lRanking,iRoleId,self.dataComparer)
		iIdx2=findSort.binarySearchRight(self.lRanking,iRoleId,self.dataComparer)
		if iIdx1==iIdx2:
			print '{} not exists'.format(iRoleId)
			return -1
		return self.lRanking.index(iRoleId)+1

	def getRoleMaxContri(self,iRoleId):
		return self.dMaxContribution.get(iRoleId,0)

	def setRoleMaxContri(self,iRoleId,iContribution):
		self.dMaxContribution[iRoleId]=iContribution

	def getAllRank(self):
		return self.lRanking


import findSort		