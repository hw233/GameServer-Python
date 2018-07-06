#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#工厂子类与工厂实例
import factory


class cFactoryCheckRoleId(factory.cFactory):
	def getProductFromDB(self,itNoRowInsertValues,iRoleId,**dData):
		if not (0<iRoleId<=c.MAX_ROLE_ID):
			raise Exception,'角色id不符合0<{}<=MAX_ROLE_ID'.format(iRoleId)
		return factory.cFactory.getProductFromDB(self,itNoRowInsertValues,iRoleId,**dData)

#角色简要工厂
class cResumeFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return centerService.resume.cResume(iRoleId).setFactory(self)

resumeFtr=cResumeFactory('centerResume')

import c
import centerService.resume
