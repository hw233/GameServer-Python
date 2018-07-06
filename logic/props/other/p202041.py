# -*- coding: utf-8 -*-
'''
改名
'''
import props.object

class cProps(props.object.cProps):
	def use(self, who):#override
		role.service.rpcReNameNotify(who, self.id, 3)


import role.service
