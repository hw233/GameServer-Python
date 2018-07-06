#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import account_pb2
import endPoint
import misc

class cService(account_pb2.main2terminal):
	@endPoint.result
	def rpcSendName(self,ep,oAccount,reqMsg):
		print reqMsg.iValue
		# import random
		# i=random.randint(1,2)
		# if i==1:
		# 	iSchool=1
		# else:
		# 	iSchool=3
		# ep.rpcCreateRole(reqMsg.iValue,iSchool)

	@endPoint.result
	def rpcRoleList(self,ep,ctrlr,reqMsg):
		print 'rpcRoleList','len(reqMsg.roles)=',len(reqMsg.roles)
		role=None
		for role in reqMsg.roles:			
			print 'Id：{}'.format(role.iRoleId)
			print '角色名：{}'.format(role.sRoleName)
			print '职业：{}'.format(role.iRoleSchool)
			print '等级：{}'.format(role.iRoleLevel)
			print '-------------------------------------'
		# if role:
		# 	ep.rpcRoleLogin(role.iRoleId)
		# else:
		# 	ep.rpcRandomName()

import c
import u
import log


import timeU
import mysqlCnt
import account
import role
import mainService
import props
import props_pb2
